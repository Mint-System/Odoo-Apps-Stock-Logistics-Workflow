# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging

from odoo import _, api, fields, models
from odoo.exceptions import UserError


_logger = logging.getLogger(__name__)


class ProductTemplate(models.Model):
    _inherit = "product.template"

    pick_and_validate_automatically = fields.Boolean("Pick/validate automatically", default=False)


    @api.constrains('pick_and_validate_automatically', 'tracking')
    def _check_pick_and_validate_automatically_not_tracked(self):
        for template in self:
            _logger.warning(f"#### template.pick_and_validate_automatically: {template.pick_and_validate_automatically}, template.tracking: {template.tracking}")
            if template.pick_and_validate_automatically and template.is_storable:
                raise UserError(_(
                    "You cannot enable 'Pick automatically' on a tracked product. "
                    "Tracked products (by Lot or Serial) must not have 'Pick automatically' enabled."
                ))