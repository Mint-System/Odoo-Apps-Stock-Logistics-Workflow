# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging

from odoo import _, api, fields, models

_logger = logging.getLogger(__name__)


class MrpProduction(models.Model):
    _inherit = "mrp.production"

    def action_confirm(self):
        res = super().action_confirm()
        
        for production in self:
            for picking in production.picking_ids:
                _logger.warning(f"### #### #### picking: {picking}")
                picking.split_and_validate_automatically()
                
        return res