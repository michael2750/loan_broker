#!/usr/bin/env python
import pika
import json

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

def declare_queue():
	channel.queue_declare(queue='loan_receiver')

def consumer():
	declare_queue()
	channel.basic_consume(callback,
	            			queue='loan_receiver',
	            			no_ack=True)
	print(' [*] Waiting for messages. To exit press CTRL+C')
	channel.start_consuming()

def callback(ch, method, properties, body):
	print(" [x] Received %r" % body)

if __name__ == '__main__':
	consumer()