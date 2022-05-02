
from werkzeug.exceptions import Forbidden, NotFound
from odoo import fields, http, tools, models,_
from odoo.http import request
from odoo.addons.http_routing.models.ir_http import slug
from odoo.addons.website.controllers.main import QueryURL
from odoo.addons.website_sale.controllers.main import WebsiteSale
PPG = 20 
PPR = 4

class Website(http.Controller):

	@http.route('/accessrestrict', type='http', auth="public", website=True)
	def restrcit_access(self):

		return request.render("website_page_security_app.accessrestrict",{})
