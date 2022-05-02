# -*- coding: utf-8 -*-
{
    'name': 'Customer Service Chatbot',
    'version': '1.0',
    'author': 'Odoo Engineering',
    'maintainer': 'Tech Support <techsupport@greensborowebservices.com>',
    'summary': 'Website Chatbot',
    'category': 'Website',
    'website': 'https://optimizemyroutes.com/',
    'description':
        """
A chatbot that can respond to customers via chat or email. This is a great way to provide answers to common questions.
======================================================================================================================

NOTE --> There is no support provided for this module. Customer Service chatbot/talkbot/IM bot that you can train to learn from the data (questions/answers) you provide. 
It can learn from Twitter responses, as well as manually training it by inputing a query sentence and a response to it, or by importing a file with the data structured for import.
With Notify phrases, one can set up an email notification to trigger to a certain user when a visitor enters a certain phrase while talking to the bot.

        """,
    'data': [
        "security/ir.model.access.csv",
        "views/im_livechat_channel_views.xml",
        "views/im_chatbot_templates.xml",
        "views/res_config.xml",
    ],
    'demo': [
    ],
    'depends': ["im_livechat", "website_livechat", 'mail'],
    'external_dependencies': {
        'python': [
            'chatterbot'
        ],
        'mongoDB': 1
    },
    'qweb': [
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    'price': 10,
    'currency': 'USD',
    'images': ['static/description/banner.png'],
    'post_init_hook': 'load_initial_chatbot_db',
    'license': 'AGPL-3',
}
