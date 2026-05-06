from odoo import api, models, fields
import logging

_logger = logging.getLogger(__name__)


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    is_partial_lot = fields.Boolean(
        string='Partial Lot',
        readonly=False,
        store=True,
    )

    # def _get_lot_reserved_qty(self):
    #     """
    #     Read reserved qty for this line's lot+location from stock.quant.
    #     Stable across versions — avoids the product_qty/reserved_qty/
    #     reserved_uom_qty/quantity_product_uom rename chain.
    #     """
    #     self.ensure_one()
    #     quants = self.env['stock.quant'].search([
    #         ('product_id', '=', self.product_id.id),
    #         ('lot_id', '=', self.lot_id.id),
    #         ('location_id', '=', self.location_id.id),
    #     ])
    #     return sum(quants.mapped('reserved_quantity'))
    #     # stock.quant.reserved_quantity is stable since v12

    # @api.depends('lot_id', 'location_id', 'product_id.tracking')
    # def _compute_is_partial_lot(self):
    #     for line in self:
    #         if (
    #             line.lot_id
    #             and line.product_id.tracking == 'lot'
    #         ):
    #             reserved = line._get_lot_reserved_qty()
    #             lot_qty = line.lot_id.product_qty
    #             line.is_partial_lot = (
    #                 reserved > 0 and reserved < lot_qty
    #             )
    #         else:
    #             line.is_partial_lot = False

    @api.onchange('lot_id')
    def _onchange_lot_id_fill_quantity(self):
        for line in self:
            if line.lot_id and line.product_id.tracking == 'lot':

                line.quantity = line.lot_id.product_qty
                line.is_partial_lot = False