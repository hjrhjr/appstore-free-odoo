# -*- coding: utf-8 -*-
# Copyright© 2016 ICTSTUDIO <http://www.ictstudio.eu>
# License: LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl)

from odoo import fields, models


class BaseModel(models.AbstractModel):
    _inherit = 'base'

    def get_base_url(self):
        self.ensure_one()
        return_val = super(BaseModel, self).get_base_url()
        if 'company_id' in self._fields:
            if self.company_id and self.company_id.base_url:
                return self.company_id.base_url
        return return_val
