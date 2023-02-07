from odoo import _, api, fields, models
import logging
_logger = logging.getLogger(__name__)
from datetime import datetime, timedelta
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools.misc import get_lang


class InventorySummary(models.Model):
    _name = 'inventory.summary'
    _description = 'Inventory Summary'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    location_id = fields.Many2one('stock.location')
    product_id = fields.Many2one('product.product')

    def _get_move_line_data(self, data=[], set_ids=[]):
        """Get stock move line data"""
        
        line_ids = self.env['stock.move.line'].search([
            ('state', 'in', ['done'])
        ])

        for line in line_ids:
            data.append({
                'product_id': line.product_id.id,
                'location_id': line.location_id.id,
            })
            set_ids.append(line.mapped('location_id.id', 'product_id.id'))

        return data, set_ids


    @api.model
    def get_data(self):
        """Generate inventory summary data"""

        # Get current data
        curr_ids = self.search([])
        curr_set_ids = curr_ids.mapped('location_id.id', 'product_id.id')

        # Reset data
        data=[]
        set_ids=[]

        # Get stock move line data
        data, set_ids = self._get_move_line_data(data, set_ids)

        # Create new entries
        self.create(list(filter(lambda d: d.mapped('location_id', 'product_id') not in set_ids, data)))

        # Update existing entries
        for curr in curr_ids:
            vals = list(filter(lambda d: d.mapped('location_id', 'product_id') == curr.mapped('location_id.id', 'product_id.id'), data))
            if vals:
                curr.write(vals[0])

        # Unlink obsolete entries
        # self.search([('product_id','not in', set_ids)]).unlink()

