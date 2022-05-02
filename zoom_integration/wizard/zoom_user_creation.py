# -*- coding: utf-8 -*-

from odoo import fields, models, api, _

from odoo.exceptions import UserError, ValidationError
import json
from zoomus import ZoomClient

class ZoomUserCreate(models.TransientModel):
    _name = "zoom.user.create"

    user_id = fields.Many2one('res.users')
    email =fields.Char('Email')
    first_name = fields.Char('First Name')
    last_name= fields.Char('Last Name')
    user_type = fields.Selection([
        ('basic', 'Basic'),
        ('licensed', 'Licensed')
    ], string='User Type', default='basic')


    @api.onchange('user_id')
    def _onchange_user_id(self):
        if self.user_id:
            name =self.user_id.name.split(" ", 1)
            self.first_name = name[0]
            if len(name) !=1:
                self.last_name=name[1]
            else:
                self.last_name=''
            self.email = self.user_id.email


    def create_zoom_user(self):
        client = self.jwt_api_access()
        if self.user_type=='basic':
            type=1
        else:
            type =2
        kwargs = {'email':self.email,
                  'type': type,
                  'first_name': self.first_name,
                  'last_name': self.last_name
                  }
        result = client.user.create(action="create",user_info=kwargs)
        result_value = json.loads(result.content.decode('utf-8'))
        if result.status_code ==201:
            self.user_id.zoom_login_email = self.email
        else:
            raise UserError(_('Zoom API Exception:\n %s.') % result_value['message'])




    def jwt_api_access(self):
        """
         Connection Zoom API using JWT App
        """
        company_rec = self.env.user.company_id
        if company_rec.api_key and company_rec.api_secret:
            try:
                client = ZoomClient(company_rec.api_key, company_rec.api_secret)

            except Exception as e:
                raise UserError(_('API credential invalid',e))

            return client
        else:
            raise UserError(_(
                'API credential invalid'))