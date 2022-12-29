from odoo import api, fields, models, _
import logging
_logger = logging.getLogger(__name__)


class StockLocation(models.Model):
    _inherit = 'stock.location'

    @api.depends('usage', 'valued_location')
    def _compute_should_be_valued(self):
        for rec in self:
            rec.should_be_valued = rec._should_be_valued()

    valued_location = fields.Boolean(string='Location is valued?', help='Mark if location should be valued. This overwrites the default behavior.')
    should_be_valued = fields.Boolean(compute=_compute_should_be_valued)

    def _should_be_valued(self):
        res = super()._should_be_valued()
        if self.valued_location:
            return False
        return res
