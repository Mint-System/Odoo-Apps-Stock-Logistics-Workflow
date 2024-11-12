from odoo import api, fields, models, _
import logging
_logger = logging.getLogger(__name__)


class StockMove(models.Model):
    _inherit = "stock.move"

    @api.depends('product_id', 'product_uom_qty', 'product_uom')
    def _cal_move_weight(self):
        weight_uom_id = self.env['product.template']._get_weight_uom_id_from_ir_config_parameter()
        moves_with_weight = self.filtered(lambda moves: moves.product_id.weight > 0.00)
        for move in moves_with_weight:
            weight_uom = move.product_id.weight_uom_id._compute_quantity(move.product_id.weight, weight_uom_id)
            # _logger.warning(["_cal_move_weight",move.product_id.weight_uom_id.name,weight_uom_id.name])
            # _logger.warning([move.product_id.weight,weight_uom])
            move.weight = (move.product_qty * weight_uom)
        (self - moves_with_weight).weight = 0
