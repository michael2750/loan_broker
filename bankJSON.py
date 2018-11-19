import pika
import json

class BankJSON(object):
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='datdb.cphbusiness.dk', port='5672'))
        self.channel = self.connection.channel()
        #self.connection_2 = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        #self.channel_2 = self.connection_2.channel()
        #self.channel_2.queue_declare(queue='hello')

        result = self.channel.queue_declare(exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(self.on_response, no_ack=True,
                                   queue=self.callback_queue)

    def on_response(self, ch, method, props, body):
        #if self.corr_id == props.correlation_id:
        #self.channel_2.basic_publish(exchange='',
        #              routing_key='hello',
        #              body=body)
        self.response = body

    def call(self, n):
        self.response = None
        self.channel.basic_publish(exchange='cphbusiness.bankJSON',
                                   routing_key='',
                                   properties=pika.BasicProperties(
                                         reply_to = self.callback_queue
                                         ),
                                   body=json.dumps(n))
        while self.response is None:
            self.connection.process_data_events()
        return self.response


def callback(ch, method, properties, body):
    json_string = json.loads(body)
    print(json.dumps(json_string))
    new_json_string = {}
    new_json_string["ssn"] = json_string["ssn"].replace("-","")
    new_json_string["loanAmount"] = float(json_string["loan_amount"])
    new_json_string["loanDuration"] = json_string["loan_duration"]
    #new_json_string["rki"] = False
    bank_json = BankJSON()
    response = bank_json.call(new_json_string)
    print(" BANKJSON [.] Got %r" % response)



connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='bankJSON_translator')

channel.basic_consume(callback,
                      queue='bankJSON_translator',
                      no_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()