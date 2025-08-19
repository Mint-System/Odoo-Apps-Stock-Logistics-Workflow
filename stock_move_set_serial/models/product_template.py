from odoo import fields, models

class ProductTemplate(models.Model):
    _inherit = "product.template"

    serial_prefix = fields.Char(
        string="Serial Number Prefix",
        help="Prefix to use when generating serial numbers (default 'SN').",
        default="SN"
    )
