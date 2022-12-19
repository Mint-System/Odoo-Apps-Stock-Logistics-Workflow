
from odoo import models, _
import logging
_logger = logging.getLogger(__name__)
from odoo.exceptions import UserError

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def action_assign(self):
        """Assign manufacturing orders."""
        for picking in self:
            mrp_production_ids = picking.move_lines.move_orig_ids.production_id
            mrp_production_ids.action_assign()
            if any(x.state != 'to_close' for x in mrp_production_ids):
                raise UserError(_('Upstream manufacturing order could not be assigned!'))
        return super().action_assign()
