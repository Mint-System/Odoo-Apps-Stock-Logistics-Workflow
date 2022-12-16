from odoo import api, fields, models, _
import logging
_logger = logging.getLogger(__name__)


class StockMove(models.Model):
    _inherit = 'stock.move'

    def _prepare_move_line_vals(self, quantity=None, reserved_quant=None):
        """
        Prepare quantity done for lines with lots.
        """
        self.ensure_one()
        res = super()._prepare_move_line_vals(quantity, reserved_quant)
        if self.quantity_done != self.product_uom_qty and res.get('lot_id'):
            res.update({'qty_done': res.get('product_uom_qty', 0.0)})
        return res

    def _action_assign(self):
        """
        Update stock move line quantity done field with reserved quantity.
        We can not use _prepare_move_line_vals method because this method only is called for a new lines.
        """
        res = super()._action_assign()
        
        for line in self.filtered(lambda m: m.state in ["confirmed", "assigned", "waiting", "partially_available"]):
            lines_to_update = line.move_line_ids.filtered(lambda l: l.qty_done != l.product_uom_qty)
            for move_line in lines_to_update:
                if move_line.lot_id:
                    move_line.qty_done = move_line.product_uom_qty or move_line.move_id.product_uom_qty
        return res
