import logging
from odoo import _, api, fields, models
_logger = logging.getLogger(__name__)

class MaintenanceEquipment(models.Model):
    _inherit = 'maintenance.equipment'

    barcode = fields.Char(copy=False, help='Unique identifier for the maintenance equipment.')