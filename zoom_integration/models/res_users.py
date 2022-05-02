# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from zoomus import ZoomClient
import json
from odoo.exceptions import UserError, ValidationError


class User(models.Model):
    """ Model for Company

             - `meeting_event_mail_notification` : disabled sending email to attendees and external users  when creating/editing/deleteing a meeting
    """

    _inherit = "res.users"

#   Userwise zoom authentication
    
    zoom_login_email=fields.Char("Zoom login mail")
    zoom_login_user_id = fields.Char("Zoom user id")
    zoom_user_timezone = fields.Char("Zoom user timezone")




