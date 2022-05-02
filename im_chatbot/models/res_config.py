# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class LiveChatConfigSettings(models.TransientModel):

    _name = 'livechat.config.settings'
    _inherit = 'res.config.settings'

    
    TWITTER_CONSUMER_KEY = fields.Char(string='Twitter consumer key', help='Enter the Twitter consumer key obtained from https://dev.twitter.com/apps.')
    TWITTER_CONSUMER_SECRET = fields.Char(string='Twitter consumer secret', help='Enter the Twitter consumer key obtained from https://dev.twitter.com/apps.')
    TWITTER_ACCESS_TOKEN = fields.Char(string='Twitter access token', help='Enter the Twitter consumer key obtained from https://dev.twitter.com/apps.')
    TWITTER_ACCESS_TOKEN_SECRET = fields.Char(string='Twitter access token secret', help='Enter the Twitter consumer key obtained from https://dev.twitter.com/apps.')

    
    def set_TWITTER_CONSUMER_KEY(self):
        ir_config_obj = self.env['ir.config_parameter']
        ir_config_obj.set_param('TWITTER_CONSUMER_KEY',
                                self.TWITTER_CONSUMER_KEY)

    def get_default_TWITTER_CONSUMER_KEY(self, fields):
        ir_config_obj = self.env['ir.config_parameter']
        val = ir_config_obj.get_param(
            'TWITTER_CONSUMER_KEY', default='')
        
        return dict(TWITTER_CONSUMER_KEY=val)
    
    def set_TWITTER_CONSUMER_SECRET(self):
        ir_config_obj = self.env['ir.config_parameter']
        ir_config_obj.set_param('TWITTER_CONSUMER_SECRET',
                                self.TWITTER_CONSUMER_SECRET)

    def get_default_TWITTER_CONSUMER_SECRET(self, fields):
        ir_config_obj = self.env['ir.config_parameter']
        val = ir_config_obj.get_param(
            'TWITTER_CONSUMER_SECRET', default='')

        return dict(TWITTER_CONSUMER_SECRET=val)
    
    def set_TWITTER_ACCESS_TOKEN(self):
        ir_config_obj = self.env['ir.config_parameter']
        ir_config_obj.set_param('TWITTER_ACCESS_TOKEN',
                                self.TWITTER_ACCESS_TOKEN)

    def get_default_TWITTER_ACCESS_TOKEN(self, fields):
        ir_config_obj = self.env['ir.config_parameter']
        val = ir_config_obj.get_param(
            'TWITTER_ACCESS_TOKEN', default='')
        
        return dict(TWITTER_ACCESS_TOKEN=val)
    
    def set_TWITTER_ACCESS_TOKEN_SECRET(self):
        ir_config_obj = self.env['ir.config_parameter']
        ir_config_obj.set_param('TWITTER_ACCESS_TOKEN_SECRET',
                                self.TWITTER_ACCESS_TOKEN_SECRET)

    def get_default_TWITTER_ACCESS_TOKEN_SECRET(self, fields):
        ir_config_obj = self.env['ir.config_parameter']
        val = ir_config_obj.get_param(
            'TWITTER_ACCESS_TOKEN_SECRET', default='')
        
        return dict(TWITTER_ACCESS_TOKEN_SECRET=val)
