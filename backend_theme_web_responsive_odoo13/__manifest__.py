# -*- coding: utf-8 -*-
# Copyright 2019, 2020 Odoo VietNam - WinERP
# Website winerp.vn, odoovietnam.com.vn
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

{
    "name": "Dependency for Material Backend Theme Odoo 13 Community",
    "version": "13.0.0.6",
    "summary": "Dependency for Material Backend Theme Odoo 13 Community. This module will be obsolete when web_responsive Odoo 13 Community is available in the Odoo Appstore.",
    "category": "Web/Backend",
    "author": "Odoo VietNam - WinERP",
    "support": "info@winerp.vn",
    "website": "https://winerp.vn",
    "license": "LGPL-3",
    'description': """
		Dependency for Material Backend Theme Odoo 13 Community. This module will be obsolete when web_responsive Odoo 13 Community is available in the Odoo Appstore.
    """,
    "depends": [
        'web',
        'mail'
    ],
    "data": [
        'views/assets.xml',
        'views/res_users.xml',
        'views/web.xml'
    ],
    'qweb': [
        'static/src/xml/apps.xml',
        'static/src/xml/form_view.xml',
        'static/src/xml/navbar.xml'
    ],
    'images':[
        'static/description/module-cover.jpg'
	],
    'installable': True,
    'auto_install': False,
    'application': False
}
