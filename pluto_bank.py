#!/usr/bin/env python
import pika
import json

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

def declare_queue():
	channel.queue_declare(queue='loan_request')
	channel.queue_declare(queue='loan_receiver')

def consumer():
	channel.basic_consume(callback,
	            			queue='loan_request',
	            			no_ack=True)
	print(' [*] Waiting for messages. To exit press CTRL+C')
	channel.start_consuming()

def callback(ch, method, properties, body):
	print(" [x] Received %r" % body)
	json_string = handle_callback_body(body)
	channel.basic_publish(exchange='',
						routing_key='loan_receiver',
						body=json_string)
	print(" [x] Sent", json_string)

def handle_callback_body(body):
	body = json.loads(body)[0]
	interest_rate = calc_interest_rate(body)
	ssn = body['ssn']
	data = {'ssn': ssn, 'interest': interest_rate}
	json_string = json.dumps(data)
	return json_string

def calc_interest_rate(body):
	credit_score = body['credit_score']
	loan_amount = body['loan_amount']
	loan_duration = body['loan_duration']
	if loan_amount > 999999:
		if loan_duration > 1825:
			interest_rate = 2
		else:
			interest_rate = 3.5
	else:
		interest_rate = 5
	return interest_rate

if __name__ == '__main__':
	declare_queue()
	data = consumer()
	send_interest_rate(data)
