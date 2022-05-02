# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Odoo Zoom Integration',
    'version': '13.0.1',
    'summary': 'Create and share Zoom video conferences with other users and external partners',
    'author': 'Fingent',
    'sequence': 2,
    'description': """
        Create and share Zoom video conference meetings between Odoo users. You can invite external users by sending mail from Odoo.
    """,
    'category': 'Extra Tools',

    'website': 'www.fingent.com',
    'images': ['static/description/cover_image.png'],
    "license": "AGPL-3",
    'depends': ['calendar','mail'],
    'data': [
            'security/ir.model.access.csv',
            'data/external_user_mail_data.xml',
            'data/mail_data.xml',
            'view/res_users_views.xml',
            'view/calendar_views.xml',
            'view/res_company_view.xml',
            'view/calendar_templates.xml',
            'wizard/zoom_user_creation.xml'

             ],
    'external_dependencies': {
        'python': ['zoomus'],
    },
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,

}
