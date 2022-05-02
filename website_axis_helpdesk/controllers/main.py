# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request
import odoo



class WebsiteManageHelpdesk(http.Controller):

    @http.route('/search_helpdesk_tickets', type='http', auth='user', website=True)
    def search_create_helpdesk_tickets_details(self , **kwargs):
        helpdesk_tickets = request.env['helpdesk.ticket'].sudo().search([])
        return  request.render('website_axis_helpdesk.search_helpdesk_ticket_page', {'ticket': helpdesk_tickets})

    @http.route(['/helpdesk/search/ticket'], type='http', methods=['POST'],auth='user', website=True, csrf=False)
    def helpdesk_search_ticket(self , **kwargs):
        ticket_id = request.env['helpdesk.ticket'].search([('number','=', kwargs.get('search'))])
        if ticket_id:
            return request.redirect('/helpdesk/ticket/%s' % (ticket_id.id))
        else:
            return request.render('website_axis_helpdesk.helpdesk_error_message', {'error_message': ticket_id})



    @http.route(['/helpdesk/form'], type='http', auth="user", website=True)
    def helpdesk_form(self, **post):
        
        helpdesk_tickets = request.env['helpdesk.ticket'].sudo().search([])
        helpdesk_tickets_type = request.env['helpdesk.ticket.type'].sudo().search([])
        partner_name = ""
        partner_email =""
        select = request.env['res.users'].search([('id','=', 2)])
        if not select:
            partner_name = http.request.env.user.name
            partner_email = http.request.env.user.email

    
        return request.render("website_axis_helpdesk.tmp_helpdesk_ticket_form", {'my_tickets': helpdesk_tickets,'ticket_types': helpdesk_tickets_type,'partner_name':partner_name,'partner_email':partner_email})



    @http.route(['/helpdesk/form/submit'], type='http', auth="user", website=True)
    def helpdesk_form_submit(self, **post):
        if not post:
           return request.redirect("/helpdesk/form")
        ticket = request.env['helpdesk.ticket'].sudo().create({
            'ticket_type_id': post.get('ticket_type_id'),
            'name': post.get('name'),
            'partner_name': post.get('partner_name'),
            'partner_email': post.get('partner_email'),
            'priority': post.get('priority'),
            'description': post.get('description'),
        })
        vals = {
            'ticket': ticket,
        }
        return request.render("website_axis_helpdesk.tmp_helpdesk_ticket_form_success", vals)



    @http.route(['/portal/get_id'], type='json', auth="user", website=True, csrf=False)
    def get_ticket_id(self, **post):
        base_value = request.params['id']
        send_data = request.env['helpdesk.ticket'].sudo().search([('id','=',base_value )])
        if request.env.is_admin():
            send_data.is_customer_replied = False
        else:
            send_data.is_customer_replied = True

       