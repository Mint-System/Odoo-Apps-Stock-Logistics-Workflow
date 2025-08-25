from odoo import fields, models, api

class ProductTemplate(models.Model):
    _inherit = "product.template"

    @api.model
    def _default_serial_prefix(self):
        return "SN" if self.tracking in ('lot', 'serial') else ""

    serial_prefix = fields.Char(
        string="Serial Number Prefix",
        help="Prefix to use when generating serial numbers (default 'SN').",
        default=_default_serial_prefix
    )
