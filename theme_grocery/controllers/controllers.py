# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.osv import expression


class website_sale(WebsiteSale):

    def _check_float(self, val):
        try:
            return float(val)
        except ValueError:
            pass
        return False

    def _get_search_domain(self, search, category, attrib_values):
        domains = super(website_sale, self)._get_search_domain(search, category, attrib_values)

        # Price
        min_price = request.httprequest.args.get('min_price')
        max_price = request.httprequest.args.get('max_price')
        if min_price:
            min_price = self._check_float(min_price)
            if min_price:
                domains = expression.AND([domains, [('list_price', '>=', min_price)]])
        if max_price:
            max_price = self._check_float(max_price)
            if max_price:
                domains = expression.AND([domains, [('list_price', '<=', max_price)]])
        if request.httprequest.args.get('under_10'):
            domains = expression.AND([domains, [('list_price', '<=', 10)]])
        if request.httprequest.args.get('ten_to_tweenty'):
            domains = expression.AND([domains, ['&',('list_price', '>=', 10), ('list_price', '<=', 20)]])
        if request.httprequest.args.get('over_20'):
            domains = expression.AND([domains, [('list_price', '>=', 20)]])

        return domains

    @http.route([
        '/shop',
        '/shop/page/<int:page>',
        '/shop/category/<model("product.public.category"):category>',
        '/shop/category/<model("product.public.category"):category>/page/<int:page>'
    ], type='http', auth="public", website=True)
    def shop(self, page=0, category=None, search='', ppg=False, **post):
        res = super(website_sale, self).shop(
            page=page, category=category, search=search, ppg=ppg, **post)

        att_items = res.qcontext.get('attrib_values')
        new_list = {}
        for item in att_items:
            if item[0] in new_list.keys():
                att_value = new_list.get(item[0])
                att_value += [item[1]]
                new_list[item[0]] = att_value
            else:
                new_list.update({item[0]: [item[1]]})

        attr_filters = {}
        for attr in new_list:
            attr_name = request.env['product.attribute'].browse(attr).name
            attr_values = []
            for att_value_id in new_list.get(attr):
                attr_value = request.env['product.attribute.value'].browse(att_value_id).name
                attr_values.append((attr_value, '%s-%s' % (attr, att_value_id)))
            attr_filters.update({attr_name: attr_values})
        res.qcontext['attr_filters'] = attr_filters
        return res

    @http.route(['/shop/cart/update_json'], type='json', auth="public", methods=['POST'], website=True, csrf=False)
    def cart_update_json(self, product_id, line_id=None, add_qty=None, set_qty=None, display=True):
        res = super(website_sale, self).cart_update_json(
            product_id=product_id, line_id=None, add_qty=add_qty, set_qty=set_qty, display=display)
        order = request.website.sale_get_order()
        if order.order_line:
            amount = "{:0.2f}".format(order.amount_total)
            res['cart_amount'] = order.currency_id.symbol + ' ' + amount
        return res

    @http.route(['/shop/cart/update_option'], type='http', auth="public", methods=['POST'],
                website=True, multilang=False)
    def cart_options_update_json(self, product_and_options, goto_shop=None, lang=None, **kwargs):
        res = super(website_sale, self).cart_options_update_json(
            product_and_options, goto_shop, lang, **kwargs)
        res = {}
        order = request.website.sale_get_order()
        if order.order_line:
            amt = "{:0.2f}".format(order.amount_total)
            amount = order.currency_id.symbol + ' ' + amt
            res = '{"cart_quantity": "%s", "cart_amount": "%s"}' % (
                str(order.cart_quantity), amount)
        return res

    @http.route(['/add/quick/views/popup'], type='json', auth="public", methods=['POST'], website=True, csrf=False)
    def quick_views_popup(self, product_id, **kw):
        values = {}
        if product_id:
            product = request.env['product.template'].browse(product_id)
            values['data'] = request.env['ir.ui.view']._render_template("theme_grocery.p_detail_quick_view_model", {
                'product': product
            })
        return values
