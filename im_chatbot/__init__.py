# -*- coding: utf-8 -*-
from . import controllers
from . import models
#import report

from odoo import api, SUPERUSER_ID

def load_initial_chatbot_db(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    env['im_livechat.channel'].load_initial_chatbot_db()