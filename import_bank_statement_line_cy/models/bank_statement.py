# -*- coding: utf-8 -*-
import base64
import binascii
import tempfile
import logging
from datetime import datetime
from odoo.exceptions import Warning, AccessError
from odoo import models, fields, api, exceptions, _

_logger = logging.getLogger(__name__)

try:
    import xlrd
except ImportError:
    _logger.debug('Cannot `import xlrd`.')


class account_bank_statement_wizard(models.TransientModel):
    _name = "account.bank.statement.wizard"

    file = fields.Many2many('ir.attachment', string='文件', required=True, help='从您的银行网站上下载对账单，然后导入。')

    def import_file(self):
        self.ensure_one()
        for data_file in self.file:
            fp = tempfile.NamedTemporaryFile(suffix=".xls")
            fp.write(binascii.a2b_base64(data_file.datas))
            fp.seek(0)
            values = {}
            try:
                workbook = xlrd.open_workbook(fp.name)
            except AccessError:
                raise Warning(_("无法打开这个excel表格。"))
            sheet = workbook.sheet_by_index(0)
            for row_no in range(sheet.nrows):
                if row_no <= 0:
                    pass
                else:
                    line = list(map(lambda row: row.value, sheet.row(row_no)))
                    if not line[0]:
                        raise Warning(_('第"%s"行单元格内没有读到日期（必填）。') % row_no)
                    date_string = line[0]
                    if not line[1]:
                        raise Warning(_('第"%s"行单元格内没有读到标签（必填）。') % row_no)
                    name = line[1]

                    values.update({
                        'date': date_string,
                        'name': name,
                        'partner': line[2],
                        'amount': line[3],
                    })
                    res = self._create_statement_lines(values)
        self.env['account.bank.statement'].browse(self._context.get('active_id'))._end_balance()
        return res

    def _create_statement_lines(self,val):
        account_bank_statement_line_obj = self.env['account.bank.statement.line']
        partner_id = self._find_partner(val.get('partner'))
        max_sequence = account_bank_statement_line_obj.search_read(
            [('statement_id', '=', self._context.get('active_id')), ('sequence', '!=', False)],
            ['sequence'], limit=1, order='sequence desc')
        max_sequence = max_sequence and max_sequence[0]['sequence'] or 0

        account_bank_statement_line_obj.create({
            'date': datetime.strptime(str(val.get('date')), '%Y%m%d'),
            'name': val.get('name'),
            'partner_id': partner_id,
            'amount': val.get('amount'),
            'statement_id': self._context.get('active_id'),
            'sequence': max_sequence + 1,
        })
        return True

    def _find_partner(self, name):
        partner_id = self.env['res.partner'].search([('name', '=', name)])
        if partner_id:
            return partner_id.id
        elif name is "":
            return name
        else:
            raise Warning(_(' "%s" 没有在联系人中找到.') % name)



