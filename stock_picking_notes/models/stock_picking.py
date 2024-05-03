from odoo import models, fields, api, _
import logging
_logger = logging.getLogger(__name__)


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    note_header = fields.Html(string='Note Header')
    note_footer = fields.Html(string='Note Footer')
