# -*- coding: utf-8 -*-

from odoo import fields, models, api, _


class ResCompany(models.Model):
    """ Model for Company

             - `meeting_event_mail_notification` : disabled sending email to attendees and external users  when creating/editing/deleteing a meeting
    """

    _inherit = "res.company"

    api_key = fields.Char("API Key")
    api_secret = fields.Char("API Secret")
    meeting_event_mail_notification=fields.Boolean("Meeting event mail notification",default=True)
    zoom_admin_user_id =fields.Many2one('res.users')



