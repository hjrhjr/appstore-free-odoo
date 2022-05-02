# -*- coding: utf-8 -*-
{
    'name': "Aged Inventory Updates",

    'description': """
    Enhance Odoo Inventory to enable the accurate date of purchase for inventory item. Ensure the accurate historical date of purchase for an inventory item can be set during import to accurately effect aged inventory reporting.
    """,

    'author': "SimplySolved",
    'company': 'SimplySolved',
    'maintainer': 'SimplySolved',
    'website': "https://www.SimplySolved.ae",
    'price': 0,
    'currency': 'USD',
    'category': 'Uncategorized',
    'version': '13.0.1.0.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'stock', 'stock_account'],

    # always loaded
    'data': [
        'views/stock_picking.xml',

    ],
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
    'images': ['static/description/main_screenshot.gif']
}
