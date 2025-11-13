import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class StockMove(models.Model):
    _inherit = "stock.move"

    product_standard_price = fields.Float(
        string="Product Standard Cost",
        # related='product_id.standard_price',
        compute="_compute_product_costs",
        store=True,
    )

    planned_costs = fields.Float(
        string="Planned Cost (Demand x Standard Price)", compute="_compute_product_costs", store=True
    )

    @api.depends("product_id", "product_uom_qty")
    def _compute_product_costs(self):
        for move in self:
            standard_price = move.product_id.standard_price
            move.product_standard_price = standard_price or 0.0
            move.planned_costs = move.product_uom_qty * standard_price
