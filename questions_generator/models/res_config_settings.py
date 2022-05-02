from odoo import fields, models, api

import logging

_logger = logging.getLogger(__name__)

PARAMS = [
    ("question_generation", "slide.qgen.settings.container.question_generation"),
    ("questgen", "slide.qgen.settings.container.questgen"),
    ("teacherpeterpan", "slide.qgen.settings.container.teacherpeterpan"),
]


class QGSecure(models.Model):
    _name = "slide.qgen.settings.container"

    question_generation = fields.Boolean(string="PATIL-SURAJ")
    questgen = fields.Boolean(string="questgen")
    teacherpeterpan = fields.Boolean(string="teacherpeterpan")


class QGResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    question_generation = fields.Boolean(
        string="PATIL-SURAJ", help="Cheapest in RAM(2 GB) and simplest")
    questgen = fields.Boolean(
        string="QUESTGEN", help="RAM(4 GB) and midle")
    teacherpeterpan = fields.Boolean(
        string="MQA-QG", help="Greediest Cheapest in RAM(8 GB) and most sofisticated")

    def get_values(self):
        res = super(QGResConfigSettings, self).get_values()
        for field_name, key_name in PARAMS:
            res[field_name] = (
                True
                if self.env["ir.config_parameter"].sudo().get_param(key_name) == "True"
                else False
            )
        return res

    def set_values(self):
        super(QGResConfigSettings, self).set_values()

        for field_name, key_name in PARAMS:
            if isinstance(self[field_name], models.BaseModel):
                if self._fields[field_name].type == "many2one":
                    value = self[field_name].id
                else:
                    value = self[field_name].ids
            else:
                value = self[field_name]
            self.env["ir.config_parameter"].set_param(key_name, value)
