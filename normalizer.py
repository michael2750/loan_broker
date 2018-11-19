import pika
import json
import xmltodict

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()


channel.queue_declare(queue='normalizer')


def callback(ch, method, properties, body):
	global channel
	json_string = {}
	print(body)
	if "<" in str(body) and ">" in str(body):
		json_string["bankXML"] = json.loads(json.dumps(xmltodict.parse(body)))
	if "{" in str(body) and "}" in str(body):
		new_json_string = json.loads(body)
		if "-" not in new_json_string["ssn"]:
			json_string["bankJSON"] = new_json_string
		if len(new_json_string["ssn"]) > 6:
			json_string["bankPluto"] = new_json_string
		else:
			json_string["saturnBank"] = new_json_string

	channel.basic_publish(exchange='',
						routing_key='aggregator',
						body=json.dumps(json_string))



channel.basic_consume(callback,
                      queue='normalizer',
                      no_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
