import logging

_logger = logging.getLogger(__name__)
from odoo import models


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    def _get_aggregated_product_quantities(self, **kwargs):
        aggregated_move_lines = super()._get_aggregated_product_quantities(**kwargs)
        _logger.warning(f"#### aggr move lines: {aggregated_move_lines}")
        for aggregated_move_line in aggregated_move_lines.values():
            move_line = aggregated_move_line["move_line"]
            _logger.warning(f"ml desc picking: {move_line.move_id.description_picking}")
            if move_line:
                aggregated_move_line[
                    "description"
                ] = move_line.move_id.description_picking.replace("\n", "<br/>")
        return aggregated_move_lines
