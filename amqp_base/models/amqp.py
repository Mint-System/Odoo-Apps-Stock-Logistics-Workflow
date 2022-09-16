from odoo import _, api, fields, models
import logging
_logger = logging.getLogger(__name__)
from pika import SelectConnection, URLParameters, BlockingConnection


class AMQPHost(models.Model):
    _name = 'amqp.host'
    _description = 'AMQP Host'

    name = fields.Char(required=True)
    url = fields.Char(required=True)


class AMQPPublisher(models.Model):
    _name = 'amqp.publisher'
    _description = 'AMQP Publisher'
    

    name = fields.Char(required=True)
    topic = fields.Char(required=True)
    routing_key = fields.Char(required=True)
    host_id = fields.Many2one('amqp.host', required=True)
    message_ids = fields.One2many('amqp.message', 'publisher_id', string='Messages')


def on_message(channel, method_frame, header_frame, body):
    _logger.warning(method_frame.delivery_tag)
    _logger.warning(body)
    channel.basic_ack(delivery_tag=method_frame.delivery_tag)

class AMQPConsumer(models.Model):
    _name = 'amqp.consumer'
    _description = 'AMQP Consumer'

    name = fields.Char(required=True)
    topic = fields.Char(required=True)
    routing_key = fields.Char(required=True)
    host_id = fields.Many2one('amqp.host', required=True)
    message_ids = fields.One2many('amqp.message', 'consumer_id', string='Messages')

    def start(self):
        url = self.host_id.url
        connection = BlockingConnection(URLParameters(url))
        channel = connection.channel()
        channel.queue_declare(queue=self.routing_key, durable=True, exclusive=False, auto_delete=False)
        channel.basic_consume(self.routing_key, on_message)
        try:
            channel.start_consuming()
        except KeyboardInterrupt:
            channel.stop_consuming()
        connection.close()