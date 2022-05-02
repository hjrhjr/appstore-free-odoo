# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Quant Package - Dimension and Gross Weight',
    'version': '13.0.0.1',
    'author': 'Global Resource Systems',
    'website': 'https://www.grs.ma',
    'license': 'LGPL-3',
    'category': 'Inventaire',
    'summary': 'Add the dimension and gross weight fields in the picking package',
    'description': """

    """,
    'depends': ['stock', 'delivery'],
    'data': [
        'views/stock_quant_package_views.xml',
    ],
    'demo': [

    ],
    'qweb': [
    ],
    'images': ['static/img/banner.png'],
    'installable': True,
    'auto_install': False
}
