from odoo import api, fields, models, _
import logging
_logger = logging.getLogger(__name__)


class StockLocation(models.Model):
    _inherit = 'stock.location'

    picking_location = fields.Boolean(string='Show Picking Location?', help='Check if location must be available in transfers.', default=False)
