
from odoo import models
import logging
_logger = logging.getLogger(__name__)
from odoo.exceptions import UserError

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def button_validate(self):
        """Validate manufacturing orders."""
        for picking in self:
            mrp_production_ids = picking.move_lines.move_orig_ids.production_id
            # _logger.warning([mrp_production_ids])
            mrp_production_ids.button_mark_done()
            if any(x.state != 'done' for x in mrp_production_ids):
                raise UserError(_('Upstream manufacturing order could not be marked as done!'))
        return super().button_validate()
