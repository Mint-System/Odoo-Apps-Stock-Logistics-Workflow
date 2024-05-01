import logging
_logger = logging.getLogger(__name__)
from odoo import _, api, fields, models


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    def _get_aggregated_product_quantities(self, **kwargs):
        """Retrieve move line using product and qty done."""
        aggregated_move_lines = super()._get_aggregated_product_quantities(**kwargs)
        # _logger.warning(aggregated_move_lines)
        for aggregated_move_line in aggregated_move_lines:
            product = aggregated_move_lines[aggregated_move_line]['product']
            move_lines = self.filtered(lambda l: l.product_id == product)
            if move_lines:
                aggregated_move_lines[aggregated_move_line]['move_line'] = move_lines[0]
            else:
                aggregated_move_lines[aggregated_move_line]['move_line'] = False
        return aggregated_move_lines
