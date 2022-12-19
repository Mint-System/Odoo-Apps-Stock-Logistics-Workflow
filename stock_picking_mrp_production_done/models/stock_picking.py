
from odoo import models, _
import logging
_logger = logging.getLogger(__name__)
from odoo.exceptions import UserError
import ast

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def button_validate(self):
        """Validate manufacturing orders."""
        assign_before = ast.literal_eval(self.env['ir.config_parameter'].sudo().get_param('stock_picking_mrp_production_done.assign_before', 'False'))
        for picking in self:
            mrp_production_ids = picking.move_lines.move_orig_ids.production_id
            if assign_before:
                mrp_production_ids.action_assign()
            mrp_production_ids.button_mark_done()
            if any(x.state != 'done' for x in mrp_production_ids):
                raise UserError(_('Upstream manufacturing order could not be marked as done!'))
        return super().button_validate()

