
# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Website Helpdesk Support Ticket in Odoo, Issue Management for customers support',
    'version': '13.2.0.0.0',
    'category': 'Operations/Helpdesk',
    'sequence': 57,
    'summary': 'Odoo website helpdesk odoo 14,13,12 and dashboard for your customer support ticket helpdesk module, ticket portal, ticket management, customer helpdesk, helpdesk ticket',
     'depends': [
        'base_setup',
        'mail',
        'utm',
        'rating',
        'web_tour',
        'resource',
        'portal',
        'digest',
        'sale_management',
        'hr',
        'sale_timesheet',
        'project',
        'account',
        'website',
        'hr_timesheet',
        'web',
        'board',
        'contacts',
    ],
    'description': """Odoo website helpdesk odoo 14,13,12 and dashboard for your customer support ticket helpdesk module, ticket portal, ticket management, customer helpdesk, helpdesk ticket
    
Helpdesk - Ticket Support App
================================

Features:

    - Process of customer tickets through different stages to solve them.
    - Add priorities, types, descriptions and tags to define your tickets.
    - Use the chatter to communicate additional information and ping co-workers on helpdesk tickets.
    - Enjoy the use of an adapted dashboard, and an easy-to-use kanban view to handle your ticket portal.
    - Make an in-depth analysis of your tickets through the pivot view in the reports menu.
    - Create a team and define its members, use an automatic assignment method if you wish.
    - Use a mail alias to automatically create tickets and communicate with your customers.
    - Add Service Level Agreement deadlines automatically to your Odoo website helpdesk Tickets.
    - Get customer feedback by using ratings.
    - Install additional features easily using your team form view.

    """,
    'data': [
        'security/helpdesk_security.xml',
        'security/ir.model.access.csv',
        'data/ticket_template.xml',
        'data/helpdesk_sequence_number.xml',
        'data/digest_data.xml',
        'data/mail_data.xml',
        'data/helpdesk_data.xml',
        'data/web_menu.xml',
        'views/helpdesk_views.xml',
        'views/helpdesk_team_views.xml',
        'views/assets.xml',
        'views/digest_views.xml',
        'views/helpdesk_portal_templates.xml',
        'views/res_partner_views.xml',
        'views/mail_activity_views.xml',
        'views/create_helpdesk_ticket.xml',
        'views/search_ticket_view.xml',
        'views/summary_view.xml',
        'report/helpdesk_sla_report_analysis_views.xml',
        'report/report.xml',
        'report/ticket_report.xml',
    ],
    'qweb': [
        "static/src/xml/helpdesk_team_templates.xml",
    ],
    'demo': ['data/helpdesk_demo.xml'],
    'application': True,
    'license': 'AGPL-3',
    'price': 42,
    'currency': 'USD',
    'support': 'business@axistechnolabs.com',
    'author': 'Axis Technolabs',
    'website': 'http://www.axistechnolabs.com',
    'images': ['static/description/images/Banner-Img.png'],
    'live_test_url':'http://helpdesk-demo.axistechnolabs.in/',
}
