import pika
import json
from sql_statements import insert_result

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

list_of_dicts = []


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
		for bank_dict in list_of_dicts:
			for key in bank_dict:
				if lowest_interest:
					if lowest_interest > bank_dict[key]["interest_rate"]:
						lowest_interest = bank_dict[key]["interest_rate"]
						ssn = bank_dict[key]["ssn"]
						bank = key
				else:
					lowest_interest = bank_dict[key]["interest_rate"]
					ssn = bank_dict[key]["ssn"]
					bank = key

		insert_result(ssn, lowest_interest, bank)
		list_of_dicts = []



channel.basic_consume(callback,
                      queue='aggregator',
                      no_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()