import pika
import json

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='bank_pluto_translator')

"""
class PlutoBank(object):
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        #self.connection_2 = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        #self.channel_2 = self.connection_2.channel()
        #self.channel_2.queue_declare(queue='hello')

        result = self.channel.queue_declare(exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(self.on_response, no_ack=True,
                                   queue=self.callback_queue)

    def call(self, n):
        self.response = None
        self.channel.basic_publish(exchange='',
                                   routing_key='loan_request',
                                   body=json.dumps(n))
"""

def callback(ch, method, properties, body):
    global channel
    json_string = json.loads(body)
    print(json.dumps(json_string))
    self.channel.basic_publish(exchange='',
                                   routing_key='loan_request',
                                   body=json.dumps(n))




channel.basic_consume(callback,
                      queue='bank_pluto_translator',
                      no_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()