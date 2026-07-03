# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging

from odoo import _, api, fields, models

_logger = logging.getLogger(__name__)


class ProductProduct(models.Model):
    # _name = "product.product"
    # _inherit = ["product.product"]
    _inherit = "product.product"