from odoo.tests import common, tagged
import logging

_logger = logging.getLogger(__name__)


@tagged('-at_install', 'post_install', 'sys')
class SystemInfoTests(common.TransactionCase):

    @classmethod
    def setUpClass(cls):
        _logger.info("setUpClass : ServerInfoTests ======")
        super().setUpClass()

        cls.ModelDataObj = cls.env['ir.http']

    def test_session_info(self):
        _logger.info("Runing Test : test_session_info ======")
        result = self.env['ir.http'].session_info()
        _logger.info(result)
        self.assertEqual(2, 1)
