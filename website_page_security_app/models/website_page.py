from odoo import fields, api, models
from odoo.http import request
from odoo.addons.http_routing.models.ir_http import _guess_mimetype
import os

import logging

_logger = logging.getLogger(__name__)


class WebsitePage(models.Model):

    _inherit = 'website.page'

    user_login_reqired = fields.Boolean(string="User Login Required")


class WebsiteMenu(models.Model):

    _inherit = "website.menu"

    user_login_reqired = fields.Boolean(
        string="User Login", compute="onchangeUserLogin")

    @api.depends('page_id.user_login_reqired')
    def onchangeUserLogin(self):
        if self.page_id.user_login_reqired is True:
            self.user_login_reqired = True
        else:
            self.user_login_reqired = False


class Http(models.AbstractModel):
    _inherit = 'ir.http'

    @classmethod
    def _serve_page(cls):
        req_page = request.httprequest.path
        page_domain = [('url', '=', req_page)] + \
            request.website.website_domain()

        published_domain = page_domain
        # specific page first
        page = request.env['website.page'].sudo().search(
            published_domain, order='website_id asc', limit=1)
        if page and (request.website.is_publisher() or page.is_visible) \
                and (page.user_login_reqired is False
                     or (page.user_login_reqired and
                         request.env.user.id != request.website.user_id.id)):
            _, ext = os.path.splitext(req_page)
            return request.render(page.get_view_identifier(), {
                'deletable': True,
                'main_object': page,
            }, mimetype=_guess_mimetype(ext))
        return False
