# -*- coding: utf-8 -*-
from odoo.addons.website_sale.controllers.main import WebsiteSale

from odoo import http


class WebsiteSale(WebsiteSale):


    @http.route([
        '''/shop''',
        '''/shop/page/<int:page>''',
        '''/shop/category/<model("product.public.category"):category>''',
        '''/shop/category/<model("product.public.category"):category>/page/<int:page>''',
        '''/slides/''',
        '''/blog/''',
        '''/partners/''',
        '''/forum/'''    
    ], type='http', auth="user", website=True, sitemap=False)
    def shop(self, page=0, category=None, search='', ppg=False, **post):
        return super().shop(page, category, search, ppg, **post)

    @http.route(['/shop/product/<model("product.template"):product>'], type='http', auth="user", website=True)
    def product(self, product, category='', search='', **kwargs):

        return super().product(product, category, search, **kwargs)
