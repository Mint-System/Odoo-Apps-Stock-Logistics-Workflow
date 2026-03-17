import logging

from odoo import models, api, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class StockMove(models.Model):
    _inherit = 'stock.move'

    @api.model
    def action_generate_lot_line_vals(self, context_data, mode, first_lot, count, lot_text):
        vals_list = super().action_generate_lot_line_vals(context_data, mode, first_lot, count, lot_text)

        if mode == 'generate' and context_data.get('default_product_id'):
            product_id = context_data['default_product_id']
            product = self.env['product.product'].browse(product_id)

            if product.default_code:
                prefix = product.default_code + '/'
                for vals in vals_list:
                    if 'lot_name' in vals:
                        vals['lot_name'] = prefix + vals['lot_name']

        return vals_list