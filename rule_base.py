import pika
import requests
import json

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()


channel.queue_declare(queue='rule_base')

def callback(ch, method, properties, body):
	json_string = json.loads(body)
	credit_score = json_string["credit_score"]
	req = requests.get("http://localhost:8000/say_hello?creditscore="+str(credit_score))
	j = json.loads(req.text)
	json_string["banks"] = j["banks"]
	channel.basic_publish(exchange='',
                      routing_key='distrabution',
                      body=json.dumps(json_string))
	print(json.dumps(json_string))

channel.basic_consume(callback,
                      queue='rule_base',
                      no_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
