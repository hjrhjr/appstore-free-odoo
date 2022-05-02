# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import base64

from odoo import http, _
from odoo.http import request, route
# from odoo.addons.base.ir.ir_qweb import AssetsBundle
from odoo import SUPERUSER_ID
from odoo.addons.bus.controllers.main import BusController


class MailChatController(BusController):
    
    def _default_request_uid(self):
        """ For Anonymous people, they receive the access right of SUPERUSER_ID since they have NO access (auth=none)
            !!! Each time a method from this controller is call, there is a check if the user (who can be anonymous and Sudo access)
            can access to the resource.
        """
        return request.session.uid and request.session.uid or SUPERUSER_ID

    # --------------------------
    # Anonymous routes (Common Methods)
    # --------------------------
    @route('/mail/chatbot_post', type="json", auth="none")
    def mail_chatbot_post(self, uuid, message_content, channel_id, **kwargs):
        request_uid = self._default_request_uid()
        
        LivechatChannel = request.env['im_livechat.channel']
        chatbot_id = LivechatChannel.sudo().browse(channel_id).chatbot_id
        chatbot_email = chatbot_id.email if chatbot_id else False
        chatbot_id = chatbot_id.id if chatbot_id else None
        
        chatbot_usage = LivechatChannel.sudo().browse(channel_id).chatbot_usage
        # chatbot responds only if it is constantly on or on when operators are offline
        if chatbot_usage == 'on' or (chatbot_usage == 'offline' and len(LivechatChannel.sudo().browse(channel_id).get_available_users()) == 0):
            # post a message without adding followers to the channel. email_from=False avoid to get author from email data
            mail_channel = request.env["mail.channel"].sudo(request_uid).search([('uuid', '=', uuid)], limit=1)
            message_response = LivechatChannel.sudo().browse(channel_id).get_chatbot_response(message_content)
            
            notify_ids = []
            request._cr.execute("""SELECT id
                                    FROM im_livechat_chatbot_notify 
                                    WHERE %(message_content)s ilike replace(name, '*', '%%')
                       """, { 'message_content': message_content})
            notify_ids.extend(request._cr.fetchall())
            if notify_ids: #catchphrase
                notify_phrases = request.env['im_livechat.chatbot_notify'].sudo(request_uid).search([('id','in', notify_ids)], limit=1)
                if isinstance(notify_phrases, list): notify_phrases = notify_phrases = notify_phrases[0]
                if (notify_phrases.notify_user_id and notify_phrases.notify_user_id.partner_id.email) or chatbot_email: 
                    mail = request.env['mail.mail'].sudo().create({
                        'body_html': message_content,
                        'subject': 'Livechat Notification: %s' % notify_phrases.name,
                        'email_to': (notify_phrases.notify_user_id and notify_phrases.notify_user_id.partner_id.email) or chatbot_email,
                        'email_from': chatbot_email or (notify_phrases.notify_user_id and notify_phrases.notify_user_id.partner_id.email),
                        'partner_ids': [(4, chatbot_id)]
                    })
                    mail.send()
            message = mail_channel.sudo(request_uid).with_context(mail_create_nosubscribe=True).message_post(author_id=chatbot_id, email_from=False, body=message_response, message_type='comment', subtype='mail.mt_comment', content_subtype='html', **kwargs)
            return message and message.id or False
        else:
            return False
    
    @http.route('/im_chatbot/init', type='json', auth="public")
    def livechat_init(self, channel_id):
        LivechatChannel = request.env['im_livechat.channel']
        available = len(LivechatChannel.browse(channel_id).get_available_users())
        chatbot_usage = LivechatChannel.sudo().browse(channel_id).chatbot_usage
        rule = {}
        # if there are operators logged in or chatbot is enabled
        if available or chatbot_usage == 'on' or (chatbot_usage == 'offline' and available == 0):
            # find the country from the request
            country_id = False
            country_code = request.session.geoip and request.session.geoip.get('country_code') or False
            if country_code:
                country_ids = request.env['res.country'].sudo().search([('code', '=', country_code)])
                if country_ids:
                    country_id = country_ids[0].id
            # extract url
            url = request.httprequest.headers.get('Referer')
            # find the first matching rule for the given country and url
            matching_rule = request.env['im_livechat.channel.rule'].sudo().match_rule(channel_id, url, country_id)
            if matching_rule:
                rule = {
                    'action': matching_rule.action,
                    'auto_popup_timer': matching_rule.auto_popup_timer,
                    'regex_url': matching_rule.regex_url,
                }
        return {
            'available_for_me': (available or chatbot_usage == 'on' or (chatbot_usage == 'offline' and available == 0)) and (not rule or rule['action'] != 'hide_button'),
            'rule': rule,
        }

