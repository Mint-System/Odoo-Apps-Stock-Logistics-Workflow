from odoo import _, fields, models


class StockQuantityHistory(models.TransientModel):
    _name = 'inventory.summary.history'
    _description = 'Inventory Summary History'

    inventory_datetime = fields.Datetime('Inventory at Date',
        help="Choose a date to get the inventory at that date",
        default=fields.Datetime.now)
    location_usage_internal = fields.Boolean('Internal Locations only', default=True)
    location_id = fields.Many2one('stock.location')

    def open_at_date(self):
        tree_view_id = self.env.ref('stock_inventory_summary.inventory_summary_list').id

        # Start calculation
        self.env['inventory.summary'].get_data(
            self.inventory_datetime,
            location_usage_internal=self.location_usage_internal,
            location_id=self.location_id
        )

        # Return to report
        action = {
            'type': 'ir.actions.act_window',
            'views': [(tree_view_id, 'tree')],
            'view_mode': 'tree',
            'name': _('Products'),
            'res_model': 'inventory.summary',
            'domain': [],
            'context': dict(self.env.context, to_date = self.inventory_datetime),
        }
        return action
