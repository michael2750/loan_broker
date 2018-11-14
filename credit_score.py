#!/usr/bin/env python
import pika
import zeep
import json

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()


channel.queue_declare(queue='credit_score')

def callback(ch, method, properties, body):
	print(" [x] Received %r" % body)
	body = json.loads(body)
	wsdl = 'http://datdb.cphbusiness.dk:8080/CreditScoreService/CreditScoreService?wsdl'
	client = zeep.Client(wsdl=wsdl)
	credit_score = client.service.creditScore(body["ssn"])
	body["credit_score"] = credit_score
	channel.basic_publish(exchange='',
			routing_key='rule_base',
			body=json.dumps(body))

channel.basic_consume(callback,
                      queue='credit_score',
                      no_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
