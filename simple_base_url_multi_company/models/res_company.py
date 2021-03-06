# -*- coding: utf-8 -*-
# CopyrightÂ© 2016 ICTSTUDIO <http://www.ictstudio.eu>
# License: LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl)

from odoo import fields, models


class ResCompany(models.AbstractModel):
    _inherit = 'res.company'

    base_url = fields.Char(string='Base URL', required=True, default='https://www.360erp.nl')
