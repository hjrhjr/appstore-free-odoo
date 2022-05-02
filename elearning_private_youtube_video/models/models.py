# -*- coding: utf-8 -*-


import base64
import datetime
import io
import re
import requests
import PyPDF2

from PIL import Image
from werkzeug import urls

from odoo import api, fields, models, _
from odoo.addons.http_routing.models.ir_http import slug
from odoo.exceptions import Warning, UserError, AccessError
from odoo.http import request
from odoo.addons.http_routing.models.ir_http import url_for


class Slide(models.Model):
    _inherit = 'slide.slide'

    @api.depends('document_id', 'slide_type', 'mime_type')
    def _compute_embed_code(self):
        base_url = request and request.httprequest.url_root or self.env['ir.config_parameter'].sudo().get_param(
            'web.base.url')
        if base_url[-1] == '/':
            base_url = base_url[:-1]
        for record in self:
            if record.datas and (not record.document_id or record.slide_type in ['document', 'presentation']):
                slide_url = base_url + url_for('/slides/embed/%s?page=1' % record.id)
                record.embed_code = '<iframe sandbox="allow-forms allow-scripts allow-pointer-lock allow-same-origin allow-top-navigation"  src="%s" class="o_wslides_iframe_viewer" allowFullScreen="true" height="%s" width="%s" frameborder="0"></iframe>' % (
                slide_url, 315, 420)
            elif record.slide_type == 'video' and record.document_id:
                if not record.mime_type:
                    # embed youtube video
                    record.embed_code = '<iframe sandbox="allow-forms allow-scripts allow-pointer-lock allow-same-origin allow-top-navigation"  src="//www.youtube.com/embed/%s?rel=0&theme=light&showinfo=0&autoplay=1"  frameborder="0"></iframe><div class="overlay"></div><div class="overlay4"></div><div class="overlay3"/></div>' % (
                        record.document_id)
                else:
                    # embed google doc video
                    record.embed_code = '<iframe sandbox="allow-forms allow-scripts allow-pointer-lock allow-same-origin allow-top-navigation"  src="//drive.google.com/file/d/%s/preview" frameborder="0"></iframe><div class="overlay"></div><div class="overlay4"></div><div class="overlay3"></div>' % (
                        record.document_id)
            else:
                record.embed_code = False
