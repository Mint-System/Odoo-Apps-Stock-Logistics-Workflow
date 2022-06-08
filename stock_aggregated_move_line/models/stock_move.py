import logging
_logger = logging.getLogger(__name__)
from odoo import _, api, fields, models


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    def _get_aggregated_product_quantities(self, **kwargs):
        aggregated_move_lines = super()._get_aggregated_product_quantities(**kwargs)
        for aggregated_move_line in aggregated_move_lines:
            product = aggregated_move_lines[aggregated_move_line]['product']
            aggregated_move_lines[aggregated_move_line]['move_line'] = self.filtered(lambda l: l.product_id == product)
        # _logger.warning(aggregated_move_lines)
        return aggregated_move_lines
