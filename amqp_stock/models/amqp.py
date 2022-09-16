from odoo import _, api, fields, models
import logging
_logger = logging.getLogger(__name__)


class AMQPHost(models.Model):
    _name = 'amqp.host'
    _description = 'AMQP Host'

    name = fields.Char(required=True)
    url = fields.Char(required=True)
