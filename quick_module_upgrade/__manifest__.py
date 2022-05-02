# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'Quick Module Upgrade',
    'version' : '13.1.0',
    'summary': 'Easy and Quickly Update your module,update module,upgrade module,easily upgrade module,module to upgrade,update,upgrade',
    'license' : 'LGPL-3',
    'support':'info@simbeez.com',
    'author':'SimBeez IT solutions LLP',
    'category':'Extra Tools',
    'description': "Easy and Quickly Update your module,update module,upgrade module,easily upgrade module,module to upgrade,update,upgrade"
    "",
    'website': 'https://simbeez.com/',
    'images': ["static/description/banner.png"],
    'depends' : ['base'],
    'data': [
            'view/quick_models_upgrade_popup_view.xml',
            'security/ir.model.access.csv',
             ],
    
    'installable': True,
    'application': False,
    'auto_install': False,
}
