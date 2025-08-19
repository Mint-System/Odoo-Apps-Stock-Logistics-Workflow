import re
import random
from odoo import api, models

import logging

_logger = logging.getLogger(__name__)

class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    def _get_next_serial(self, default_prefix="SN"):
        product = self.product_id
        _logger.warning("########### product: %s", product)
        Lot = self.env['stock.lot']
        product_lots = Lot.search([('product_id', '=', product.id)], order="name desc")
        _logger.warning("########### product_lots: %s", product_lots)
        for _lot in product_lots:
            _logger.warning("########### _lot: %s", _lot.name)

        prefix_candidate = None
        num_candidate = 0
        width_candidate = 0

        for lot in product_lots:
            m = re.search(r'^(.*?)(\d+)$', lot.name or "")
            if m:
                prefix, num_str = m.groups()
                num = int(num_str)
                if num > num_candidate:
                    num_candidate = num
                    prefix_candidate = prefix
                    width_candidate = len(num_str)

        if prefix_candidate is None:
            prefix_candidate = product.serial_prefix or default_prefix

            num_candidate = 0
            width_candidate = 6  # default padding

        next_num = str(num_candidate + 1).zfill(width_candidate)
        return f"{prefix_candidate}{next_num}"


    @api.model
    def default_get(self, fields_list):
        _logger.warning("########### default_get called")
        res = super().default_get(fields_list)
        _logger.warning("########### res: %s", res)
        # res['lot_name'] = self._get_next_serial()
        res['lot_name'] = f"SN{random.randint(10000, 99999)}"
        return res
