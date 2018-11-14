import pika
import requests
import json
import datetime

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()


channel.queue_declare(queue='distrabution')

def bankXML(json_string):
	XML_conn = pika.BlockingConnection(pika.ConnectionParameters(host='datdb.cphbusiness.dk', port='5672'))
	XML_channel = XML_conn.channel()
	queue = channel.queue_declare().method.queue

	def on_response(ch, method, props, body):
		print(" [x] Received %r" % body)

	ssn = json_string["ssn"]
	cs = json_string["credit_score"]
	loan_amount = json_string["loan_amount"]
	duration = datetime.datetime.now() + datetime.timedelta(days=json_string["loan_duration"])
	channel.basic_publish(exchange='cphbusiness.bankXML',
                      routing_key='',
                      body=f"""<LoanRequest>
							<ssn>{ssn}</ssn>
							<creditScore>{cs}</creditScore>
							<loanAmount>{loan_amount}</loanAmount>
							<loanDuration>{duration}</loanDuration>
							</LoanRequest>""")

# 1973-01-01 01:00:00.0 CET

def callback(ch, method, properties, body):
	json_string = json.loads(body)
	print(json.dumps(json_string))
	for bank in json_string["banks"]:
		if bank == "Amagerbanken":
			bankXML(json_string)
		if bank == "Nordea":
			pass
		if bank == "Banknordic":
			pass
		if bank == "Danskebank":
			pass
	channel.basic_publish(exchange='',
                      routing_key='distrabution',
                      body=json.dumps(json_string))
	

channel.basic_consume(callback,
                      queue='distrabution',
                      no_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()