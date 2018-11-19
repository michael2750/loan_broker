import pika
import json
from sql_statements import insert_result

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

list_of_dicts = {}


channel.queue_declare(queue='aggregator')

def callback(ch, method, properties, body):
	global list_of_dicts
	print(body)
	json_string = json.loads(body)
	list_of_dicts.append(json_string)
	if len(list_of_dicts) == 4:
		lowest_interest = None
		ssn = None
		bank = None
		for x,y in list_of_dicts.items():
			if lowest_interest:
				if lowest_interest > y["interest_rate"]:
					lowest_interest = y["interest_rate"]
					ssn = y["ssn"]
					bank = x
			else:
				lowest_interest = y["interest_rate"]
				ssn = y["ssn"]
				bank = x

		insert_result(ssn, lowest_interest, bank)
		list_of_dicts = {}



channel.basic_consume(callback,
                      queue='aggregator',
                      no_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()