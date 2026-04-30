from odoo import models, fields, api
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)


class StockLot(models.Model):
    _inherit = 'stock.lot'

    @api.model
    def action_move_all_lots(self):
        # check if internal transfer route exists
        picking_type = self.env['stock.picking.type'].search([
            ('code', '=', 'internal'),
            ('company_id', '=', self.env.user.company_id.id)
        ], limit=1)

        if not picking_type:
            raise UserError("No Internal Transfer Picking Type found for this company.")
            
        # filter quants with lot, tracking type = lot, quantity and no package
        quants = self.env['stock.quant'].search([
            ('lot_id', '!=', False),
            ('quantity', '>', 0),
            ('lot_id.product_id.tracking', '=', 'lot'),
            ('package_id', '=', False)
        ], order='lot_id, location_id')

        if not quants:
            raise UserError('No loose lots/quants found to process.')

        # Grouping quants due to lot
        lot_groups = {}
        for quant in quants:
            lot = quant.lot_id
            if lot not in lot_groups:
                lot_groups[lot] = []
            lot_groups[lot].append(quant)
            
        # Looping over grouped lots
        counter = 0
        for lot, lot_quants in lot_groups.items():
            if not lot_quants:
                continue
            
            # determine location for package
            sorted_quants = sorted(lot_quants, key=lambda q: q.location_id.id)
            target_location = sorted_quants[0].location_id
            
            package_name = lot.name
            
            # check package
            existing_pkg = self.env['stock.package'].search([
                ('name', '=', package_name)
            ], limit=1)
            
            if existing_pkg:
                new_pkg = existing_pkg
            else:
                new_pkg = self.env['stock.package'].create({
                    'name': package_name,
                    'location_id': target_location.id,
                })
                
            # separate quants
            quants_to_move = self.env['stock.quant']
            quants_already_at_target = self.env['stock.quant']
            
            for quant in lot_quants:
                if quant.location_id == target_location:
                    quants_already_at_target |= quant
                else:
                    quants_to_move |= quant
                    
            # moving quants to target and package
            if quants_to_move:
                try:
                    quants_to_move.move_quants(
                        location_dest_id=target_location.id,
                        package_dest_id=new_pkg.id,
                        message=f"Auto-relocation for Lot {lot.name}"
                    )
                    _logger.info(f"Relocated {len(quants_to_move)} quants for Lot {lot.name} to {target_location.name} in Package '{package_name}'")
                    counter += len(quants_to_move)
                except Exception as e:
                    _logger.error(f"Error relocating Lot {lot.name}: {str(e)}")
                    
            # assign package to quants
            if quants_already_at_target:
                try:
                    quants_already_at_target.write({
                        'package_id': new_pkg.id,
                    })
                    _logger.info(f"Assigned package to {len(quants_already_at_target)} existing quants for Lot {lot.name}")
                    counter += len(quants_already_at_target)
                except Exception as e:
                    _logger.error(f"Error assigning package for Lot {lot.name}: {str(e)}")

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Moving Complete',
                'message': 'Successfully moved %d quants with lot into packages' % counter,
                'type': 'success',
                'sticky': False,
            }
        }