from odoo import _, api, fields, models
import logging
_logger = logging.getLogger(__name__)
from pika import BlockingConnection, URLParameters, spec
from odoo.exceptions import UserError


class AMQPMessage(models.Model):
    _name = 'amqp.message'
    _description = 'AMQP Message'

    body = fields.Text(required=True)
    result = fields.Text(readonly=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('received', 'Received'),
        ('consumed', 'Consumed')],
        copy=False,
        default='draft',
        readonly=True,
        required=True)
    publisher_id = fields.Many2one('amqp.publisher')
    consumer_id = fields.Many2one('amqp.publisher')

    def publish(self):
        try:
            url = self.publisher_id.host_id.url
            connection = BlockingConnection(URLParameters(url))
            channel = connection.channel()
            result = channel.basic_publish(**self._generate_amqp_data())
            self.write({
                'result': result
            })
            connection.close()
        except Exception as e:
            raise UserError(e)
    
    def _generate_amqp_data(self):
        return {
            'exchange': self.publisher_id.topic,
            'routing_key': self.publisher_id.routing_key,
            'body': self.body,
            'properties': spec.BasicProperties(),
            'mandatory': False,
        }