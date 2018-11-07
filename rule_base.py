import pika
import requests
import json

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()


channel.queue_declare(queue='rule_base')

def callback(ch, method, properties, body):
	url = "localhost:5004/rule_base"
	data = {'credit_score': body['credit_score']}
	headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
	

	req = requests.get(url, data=json.loads(data),headers=headers)
	for key, value in json.loads(req.body).items():
		body[key] = value

    channel.basic_publish(exchange='',
                      routing_key='distrabution',
                      body=body)

channel.basic_consume(callback,
                      queue='rule_base',
                      no_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()