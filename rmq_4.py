import pika
import uuid

class FibonacciRpcClient(object):
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='datdb.cphbusiness.dk', port='5672'))
        self.channel = self.connection.channel()
        self.connection_2 = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel_2 = self.connection_2.channel()
        self.channel_2.queue_declare(queue='hello')

        result = self.channel.queue_declare(exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(self.on_response, no_ack=True,
                                   queue=self.callback_queue)

    def on_response(self, ch, method, props, body):
        print(str(body))
        #if self.corr_id == props.correlation_id:
        self.channel_2.basic_publish(exchange='',
                      routing_key='hello',
                      body=body)
        self.response = body

    def call(self, n):
        self.response = None
        self.channel.basic_publish(exchange='cphbusiness.bankJSON',
                                   routing_key='',
                                   properties=pika.BasicProperties(
                                         reply_to = self.callback_queue
                                         ),
                                   body=str(n))
        while self.response is None:
            self.connection.process_data_events()
        return self.response

fibonacci_rpc = FibonacciRpcClient()

print(" [x] Requesting fib(30)")
response = fibonacci_rpc.call('''
  {"ssn":1605789787,
  "loanAmount":10.0,
  "loanDuration":360}''')
print(" [.] Got %r" % response)
