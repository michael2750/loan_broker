import pika
import requests
import json
import datetime

class FibonacciRpcClient(object):
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
        print(str(body))
        #if self.corr_id == props.correlation_id:
        #self.channel_2.basic_publish(exchange='',
        #              routing_key='hello',
        #              body=body)
        self.response = body

    def call(self, n):
        self.response = None
        self.channel.basic_publish(exchange='cphbusiness.bankXML',
                                   routing_key='',
                                   properties=pika.BasicProperties(
                                         reply_to = self.callback_queue
                                         ),
                                   body=str(n))
        while self.response is None:
            self.connection.process_data_events()
        return self.response


connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()


channel.queue_declare(queue='distrabution')

def bankXML(json_string):
	ssn = json_string["ssn"].replace("-","")[:-2]
	cs = json_string["credit_score"]
	loan_amount = json_string["loan_amount"]
	duration = datetime.datetime.now() + datetime.timedelta(days=json_string["loan_duration"])
	fibonacci_rpc = FibonacciRpcClient()
	response = fibonacci_rpc.call(f"""<LoanRequest>
							<ssn>{ssn}</ssn>
							<creditScore>{cs}</creditScore>
							<loanAmount>{loan_amount}</loanAmount>
							<loanDuration>{duration}</loanDuration>
							</LoanRequest>""")
	print(" [.] Got %r" % response)

# 1973-01-01 01:00:00.0 CET

def callback(ch, method, properties, body):
	json_string = json.loads(body)
	print(json.dumps(json_string))
	for bank in json_string["banks"]:
		if bank == "Amagerbanken":
			pass
		if bank == "Nordea":
			pass
		if bank == "Banknordic":
			bankXML(json_string)
		if bank == "Danskebank":
			pass
	

channel.basic_consume(callback,
                      queue='distrabution',
                      no_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()