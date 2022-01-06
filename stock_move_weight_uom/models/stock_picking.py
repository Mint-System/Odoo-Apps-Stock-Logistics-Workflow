from odoo import api, fields, models, _
import logging
_logger = logging.getLogger(__name__)


class StockMove(models.Model):
    _inherit = "stock.picking"

    @api.depends('move_line_ids', 'move_line_ids.result_package_id', 'move_line_ids.product_uom_id', 'move_line_ids.qty_done')
    def _compute_bulk_weight(self):
        weight_uom_id = self.env['product.template']._get_weight_uom_id_from_ir_config_parameter()
        for picking in self:
            weight = 0.0
            for move_line in picking.move_line_ids:
                if move_line.product_id and not move_line.result_package_id:
                    weight_uom = move_line.product_id.weight_uom_id._compute_quantity(move_line.product_id.weight, weight_uom_id)
                    # _logger.warning(["_compute_bulk_weight",move_line.product_id.weight_uom_id.name,weight_uom_id.name])
                    # _logger.warning([move_line.product_id.weight,weight_uom])
                    weight += move_line.product_uom_id._compute_quantity(move_line.qty_done, move_line.product_id.uom_id) * weight_uom
            picking.weight_bulk = weight