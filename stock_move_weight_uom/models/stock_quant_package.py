from odoo import models, fields, api, _
import logging
_logger = logging.getLogger(__name__)


class StockQuantPackage(models.Model):
    _inherit = "stock.quant.package"

    @api.depends('quant_ids')
    def _compute_weight(self):
        for package in self:
            weight = 0.0
            weight_uom_id = self.env['product.template']._get_weight_uom_id_from_ir_config_parameter()
            if self.env.context.get('picking_id'):
                # TODO: potential bottleneck: N packages = N queries, use groupby ?
                current_picking_move_line_ids = self.env['stock.move.line'].search([
                    ('result_package_id', '=', package.id),
                    ('picking_id', '=', self.env.context['picking_id'])
                ])
                for ml in current_picking_move_line_ids:
                    weight_uom = ml.product_id.weight_uom_id._compute_quantity(ml.product_id.weight, weight_uom_id)
                    # _logger.warning(["_compute_weight_1",ml.product_id.weight_uom_id.name,weight_uom_id.name])
                    # _logger.warning([ml.product_id.weight,weight_uom])
                    weight += ml.product_uom_id._compute_quantity(ml.qty_done, ml.product_id.uom_id) * weight_uom
            else:
                for quant in package.quant_ids:
                    weight_uom = quant.product_id.weight_uom_id._compute_quantity(quant.product_id.weight, weight_uom_id)
                    # _logger.warning(["_compute_weight_2",quant.product_id.weight_uom_id.name,weight_uom_id.name])
                    # _logger.warning([quant.product_id.weight,weight_uom])
                    weight += quant.quantity * weight_uom
            package.weight = weight