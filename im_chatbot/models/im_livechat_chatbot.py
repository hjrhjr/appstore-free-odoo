# -*- coding: utf-8 -*-
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer, ChatterBotCorpusTrainer # TwitterTrainer
from chatterbot.logic import BestMatch #LowConfidenceAdapter

import csv
import base64
import random
import re

import odoo
from odoo import api, fields, models, modules, tools, exceptions, registry, SUPERUSER_ID, _
from odoo.exceptions import UserError

try:
    from cStringIO import StringIO
except ImportError:
    from io import StringIO


def set_chatbot_instance(lowconf_threshold, lowconf_response):
    global bot
    import unicodedata
    # Create a new instance of a ChatBot
    bot = ChatBot(
        "ChatBot",
        storage_adapter="chatterbot.storage.MongoDatabaseAdapter",
        logic_adapters=[
            {
                'import_path': 'chatterbot.logic.BestMatch'
            },
            {
                'import_path': 'chatterbot.logic.LowConfidenceAdapter',
                'threshold': (lowconf_threshold / 100.00),
                'default_response': unicodedata.normalize('NFKD', lowconf_response).encode('ascii', 'ignore') #'I am sorry, but I do not understand.'
            }
        ],
        input_adapter="chatterbot.input.VariableInputTypeAdapter",
        output_adapter="chatterbot.output.OutputAdapter",
        trainer = 'chatterbot.trainers.ListTrainer'
    )

# Uncomment the following lines to enable verbose logging
# import logging
# logging.basicConfig(level=logging.INFO)

try:
    # Create a new instance of a ChatBot
    lc_threshold = 0.65
    lc_default_response = 'I am sorry, but I do not understand.'
    bot = ChatBot(
        "ChatBot",
        storage_adapter="chatterbot.storage.MongoDatabaseAdapter",
        logic_adapters=[
            {
                'import_path': 'chatterbot.logic.BestMatch'
            },
            {
                'import_path': 'chatterbot.logic.LowConfidenceAdapter',
                'threshold': lc_threshold,
                'default_response': lc_default_response
            }
        ],
        input_adapter="chatterbot.input.VariableInputTypeAdapter",
        output_adapter="chatterbot.output.OutputAdapter",
        trainer = 'chatterbot.trainers.ListTrainer'
    )
except:
    bot = {}

class ImLivechatChatbot(models.Model):
    """ Chatbot Configuration fields
    """

    _inherit = 'im_livechat.channel'

    chatbot_usage = fields.Selection([('on', 'Always On'), ('offline', 'On when operators are offline'), ('off', 'Off')],
        string='Chatbot Usage', required=True, default='off',
        help="* 'Enable the chat bot:\n"\
             "* 'Always on - it will respond to visitors always, no matter if there are operators logged in.\n"\
             "* 'On when operators are offline - it will respond to visitors when Odoo operators are not logged in.\n"\
             "* 'Off - chat bot is turned off.")
    chatbot_id = fields.Many2one(
        'res.partner', 'Chatbot name', 
        help="The name of the chatbot (partner record), as it will appear in the chat window to the visitors.")
    chatbot_lowconfidence_threshold = fields.Float(string='Low Confidence Threshold', help='Enter a percentage (0-100) threshold for the chatbot to give a default unknown response, specified below.', required=True, default=65)
    chatbot_lowconfidence_response = fields.Char(string='Low Confidence Response', help="Enter a default response the chatbot will resort to when it can't find a response above the threshold level above.", required=True, default='I am sorry, but I do not understand.')

    @api.model
    def get_chatbot_response(self, input_sentence=''):
        
        try:
            if bot and (self.chatbot_lowconfidence_response != lc_default_response or (self.chatbot_lowconfidence_threshold/100.00) != lc_threshold):
                self.action_set_low_confidence()
            response = bot.get_response(input_sentence)
        except:
            if not bot.default_conversation_id:
                bot.default_conversation_id = bot.storage.create_conversation()
                conversation_id = bot.default_conversation_id
            else:
                conversation_id = bot.default_conversation_id
            input_statement = bot.input.process_input_statement(input_sentence)
            # Preprocess the input statement
            for preprocessor in bot.preprocessors:
                input_statement = preprocessor(bot, input_statement)
            statement_test, response_test = bot.generate_response(input_statement, conversation_id)
            if not bot.read_only:
                bot.learn_response(statement_test, statement_test)
                bot.storage.add_to_conversation(conversation_id, statement_test, response_test)
            
            response = bot.get_response(input_sentence)

        
        if '[company_email]' in response.text:
            response.text = response.text.replace('[company_email]', str( '<a href="mailto:' + self.env.user.company_id.email + '" target="_top">' + self.env.user.company_id.email + '</a>'))
        if '[product_' in response.text:
            product_ids = re.findall(r'(\[product_([0-9]+)\])+', response.text)
            for product_id_tuple in product_ids:
                product_id = product_id_tuple[1]
                product = self.env['product.template'].browse(int(product_id))
                product_url = str( '<a href="' + "/shop/product/%s" % (product_id,) + '" >' + product.name + '</a>')
                response.text = response.text.replace(product_id_tuple[0], product_url)

        final_response = self.check_for_chatbot_actions(input_sentence, response) # extended in im_chatbot_actions module
        if final_response and isinstance(final_response, list): final_response = final_response[0]
        return final_response

    #@api.one
    def check_for_chatbot_actions(self, query, response):
        return response

    def load_initial_chatbot_db(self):
        bot.set_trainer(ChatterBotCorpusTrainer)
        bot.train("chatterbot.corpus.english")
    
    @api.model
    def get_livechat_info(self, channel_id, username='Visitor'):
        info = {}
        info['available'] = (len(self.sudo().browse(channel_id).get_available_users()) > 0) or self.sudo().browse(channel_id).chatbot_usage in ['on','offline']
        info['server_url'] = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        if info['available']:
            info['options'] = self.sudo().get_channel_infos(channel_id)
            info['options']["default_username"] = username
        return info

    @api.model
    def get_mail_channel(self, livechat_channel_id, anonymous_name):
        """ Return a mail.channel given a livechat channel. It creates one with a connected operator, or return false otherwise
            :param livechat_channel_id : the identifier if the im_livechat.channel
            :param anonymous_name : the name of the anonymous person of the channel
            :type livechat_channel_id : int
            :type anonymous_name : str
            :return : channel header
            :rtype : dict
        """
        # get the avalable user of the channel
        users = self.sudo().browse(livechat_channel_id).get_available_users()
        # chatbot active or not:
        chatbot_usage = self.sudo().browse(livechat_channel_id).chatbot_usage
        
        if len(users) == 0 and chatbot_usage == 'off':
            return False
        channel_partner_to_add = []
        if chatbot_usage == 'on' or (chatbot_usage == 'offline' and len(users)==0):
            # get the chatbot partner id
            operator_partner_id = self.sudo().browse(livechat_channel_id).chatbot_id.id
            user_or_chatbot_name = self.sudo().browse(livechat_channel_id).chatbot_id.name
            for res_user in self.sudo().browse(livechat_channel_id).user_ids:
                channel_partner_to_add.append((4, res_user.partner_id.id))
        else:
            # choose the res.users operator and get its partner id
            user = random.choice(users)
            operator_partner_id = user.partner_id.id
            user_or_chatbot_name = user.name
        # partner to add to the mail.channel
        channel_partner_to_add.append((4, operator_partner_id))
        if self.env.user and self.env.user.active:  # valid session user (not public)
            channel_partner_to_add.append((4, self.env.user.partner_id.id))
        # create the session, and add the link with the given channel
        mail_channel = self.env["mail.channel"].with_context(mail_create_nosubscribe=False).sudo().create({
            'channel_partner_ids': channel_partner_to_add,
            'livechat_channel_id': livechat_channel_id,
            'anonymous_name': anonymous_name,
            'channel_type': 'livechat',
            'name': ', '.join([anonymous_name, user_or_chatbot_name]),
            'public': 'private',
            'email_send': False
        })
        return mail_channel.sudo().with_context(im_livechat_operator_partner_id=operator_partner_id).channel_info()[0]

    #@api.multi
    def action_set_low_confidence(self):
        if self.chatbot_lowconfidence_threshold < 0 or self.chatbot_lowconfidence_threshold > 100:
            raise UserError(_('Please set the threshold to a number ranging from 0 to 100!'))
        set_chatbot_instance(self.chatbot_lowconfidence_threshold, self.chatbot_lowconfidence_response)
        return True

class ImLivechatChatbotTraining(models.TransientModel):
    """ Chatbot Training Data
    """

    _name = 'im_livechat.chatbot_training'
    _description = 'Chatbot Training Data'


    input_sentence = fields.Char('Input', help="Input query.")
    response_sentence = fields.Char('Response', help="Response to the input query.")
    
    data_file = fields.Binary(string='File', help='Must be .csv format.')
    filename = fields.Char()
    
    file_save_name = fields.Char(string='Exported DB File Name')
    file_save = fields.Binary(string='Exported Chatbot Database File', readonly=True)
    
    train_lang = fields.Selection([('bangla', 'Bangla'),
                                    ('chinese', 'Chinese'),
                                    ('english', 'English'),
                                    ('french', 'French'),
                                    ('german', 'German'),
                                    ('hebrew', 'Hebrew'),
                                    ('hindi', 'Hindi'),
                                    ('indonesia', 'Indonesia'),
                                    ('italian', 'Italian'),
                                    ('marathi', 'Marathi'),
                                    ('odia', 'Odia'),
                                    ('portuguese', 'Portuguese'),
                                    ('russian', 'Russian'),
                                    ('spanish', 'Spanish'),
                                    ('swedish', 'Swedish'),
                                    ('tchinese', 'Traditional Chinese'),
                                    ('telugu', 'Telugu'),
                                    ('thai', 'Thai')], string='Initial language data to load', default='english')
    
    #@api.one
    def action_train(self):
        
        if not self.input_sentence or not self.response_sentence:
            raise exceptions.Warning(_(
                'You have not entered the input and response sentences'))
            
        conversation = [ self.input_sentence, self.response_sentence ]
        
        bot.set_trainer(ListTrainer)
        bot.train(conversation)
        
        self.input_sentence = self.response_sentence
        self.response_sentence = None
        return True
    
    #@api.one
    def action_train_from_file(self):
        import json
        if not self.data_file:
            raise exceptions.Warning(_(
                'Please select a file to upload.'))
        
        if self.filename[-3:] == 'csv':
            csv_data = base64.b64decode(self.data_file)
            data_iterator = csv.reader(
                StringIO(csv_data), quotechar='"', delimiter=',')
    
            conversation = [row[0] for row in data_iterator]
            
            bot.set_trainer(ListTrainer)
            bot.train(conversation)
        elif self.filename[-3:] == 'yml':
            yml_data = base64.b64decode(self.data_file)
            data_iterator = json.loads(yml_data)
            
            for conversation in data_iterator:
                bot.set_trainer(ListTrainer)
                bot.train(conversation)
        
        return True
    
    #@api.one
    def action_export_db(self):
        import json
        chatbot_db_data = bot.trainer._generate_export_data()
        chatbot_db_data = json.dumps(chatbot_db_data, sort_keys=True, indent=1, separators=(',', ': '))
        num = 1
        if self.file_save_name:
            try:
                num = int(self.file_save_name[-5:-4])+1
            except:
                num = 1
        self.write({'file_save_name': 'chatbot_db' + str(num) + '.yml',
                    'file_save': base64.encodestring(chatbot_db_data)})
        return {
              'type': 'ir.actions.client',
              'tag': 'reload',
        }
    
    #@api.one
    def action_drop_db(self):
        import json
        chatbot_db_data = bot.trainer._generate_export_data()
        chatbot_db_data = json.dumps(chatbot_db_data, sort_keys=True, indent=4, separators=(',', ': ')) 
        num = 1
        if self.file_save_name:
            try:
                num = int(self.file_save_name[-5:-4])+1
            except:
                num = 1
        self.write({'file_save_name': 'chatbot_db' + str(num) + '.yml',
                    'file_save': base64.encodestring(chatbot_db_data)})
        
        bot.storage.drop()
        return True
    
    #@api.one
    def action_load_initial_english(self):
        bot.set_trainer(ChatterBotCorpusTrainer)
        bot.train("chatterbot.corpus." + self.train_lang or "english")
        return True
    
    #@api.one
    def action_train_from_twitter(self):
        ir_config_param = self.env['ir.config_parameter']
        TWITTER = {
            "CONSUMER_KEY": ir_config_param.get_param('TWITTER_CONSUMER_KEY') or False,
            "CONSUMER_SECRET": ir_config_param.get_param('TWITTER_CONSUMER_SECRET') or False,
            "ACCESS_TOKEN": ir_config_param.get_param('TWITTER_ACCESS_TOKEN') or False,
            "ACCESS_TOKEN_SECRET": ir_config_param.get_param('TWITTER_ACCESS_TOKEN_SECRET') or False
        }
        if TWITTER["CONSUMER_KEY"]:
            try:
                bot.set_trainer(TwitterTrainer, twitter_consumer_key=TWITTER["CONSUMER_KEY"], twitter_consumer_secret=TWITTER["CONSUMER_SECRET"], twitter_access_token_key=TWITTER["ACCESS_TOKEN"], twitter_access_token_secret=TWITTER["ACCESS_TOKEN_SECRET"])
                bot.train()
            except Exception as e:
                raise UserError(_('There was an error with the Twitter data. Please try again. \n\n(%s).') % e)
                
        return True


class ImLivechatChatbotNotifyPhrases(models.Model):
    """ Chatbot Notify Phrases
    """

    _name = 'im_livechat.chatbot_notify'
    _description = 'Chatbot Notify Phrases'

    name = fields.Char('Phrase', required=True, help="Sentence or a part of the sentence which triggers the e-mail notification.")
    notify_user_id = fields.Many2one('res.users', string='User To Notify', help="User which will receive the e-mail notification.", default=lambda self: self.env.user)
    
