from odoo import models
import logging
_logger = logging.getLogger(__name__)


class ReplenishmentReport(models.AbstractModel):
    """Inherit from odoo/addons/stock/report/report_stock_forecasted.py"""
    _inherit = 'report.stock.report_product_product_replenishment'

    def _compute_draft_quantity_count(self, product_template_ids, product_variant_ids, wh_location_ids):
        """Include minim stock from orderpoint."""
        res = super()._compute_draft_quantity_count(product_template_ids, product_variant_ids, wh_location_ids)
        if product_template_ids:
            product_templates = self.env['product.template'].browse(product_template_ids)
            min_qty = sum(product_templates.mapped('orderpoint_ids.product_min_qty'))
            res['min_qty'] = min_qty
            res['virtual_available'] = sum(product_templates.mapped('virtual_available'))-min_qty
        elif product_variant_ids:
            product_variants = self.env['product.product'].browse(product_variant_ids)
            min_qty = sum(product_variants.mapped('orderpoint_ids.product_min_qty'))
            res['min_qty'] = min_qty
            res['virtual_available'] = sum(product_variants.mapped('virtual_available'))-min_qty
        return res

    # def _prepare_report_line(self, quantity, move_out=None, move_in=None, replenishment_filled=True, product=False, reservation=False):
    #     res = super()._prepare_report_line(quantity, move_out, move_in, replenishment_filled, product, reservation)
    #     _logger.warning(res)
    #     return res