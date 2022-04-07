from odoo import models, fields, api, _
import logging
_logger = logging.getLogger(__name__)


class StockMove(models.Model):
    _inherit = "stock.move"

    def _get_new_picking_values(self):
        vals = super()._get_new_picking_values()
        note_header = self.sale_line_id.order_id.note_header
        note_footer = self.sale_line_id.order_id.note_footer
        if note_header:
            vals.update({"note_header": note_header})
        if note_footer:
            vals.update({"note_footer": note_footer})
        return vals
