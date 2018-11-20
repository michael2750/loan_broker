import pika
import json
from sql_statements import insert_result
from threading import Thread
import datetime

list_of_dicts = []

def commit(list_of_dicts):
	lowest_interest = None
	ssn = None
	bank = None
	for bank_dict in list_of_dicts:
		for key in bank_dict:
			if lowest_interest:
				if lowest_interest > bank_dict[key]["interest_rate"]:
					lowest_interest = bank_dict[key]["interest_rate"]
					bank = key
			else:
				lowest_interest = bank_dict[key]["interest_rate"]
				bank = key
			if key == "bankPluto":
				ssn = bank_dict[key]["ssn"]

	insert_result(ssn, lowest_interest, bank)
	list_of_dicts = []

def thread_method(threadname, list_of_dicts):
	connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
	channel = connection.channel()

	channel.queue_declare(queue='aggregator')

	def callback(ch, method, properties, body):
		print(body)
		json_string = json.loads(body)
		list_of_dicts.append(json_string)
		if len(list_of_dicts) == 4:
			commit(list_of_dicts)
			

	channel.basic_consume(callback,
	                      queue='aggregator',
	                      no_ack=True)

	print(' [*] Waiting for messages. To exit press CTRL+C')
	channel.start_consuming()

thread = Thread(target=thread_method, args='thread', list_of_dicts)

ssn_dict = {}
while True:
	if len(list_of_dicts) > 0:
		for bank_dict in list_of_dicts:
			for x, y in bank_dict.items():
				if y["ssn"] not in ssn_dict:
					ssn_dict[y["ssn"]] = datetime.datetime.now()
	for x,y in ssn_dict.items():
		time_stamp = datetime.datetime.now()
		diff = (time_stamp - y).total_seconds()
		if diff > 2:
			commit(list_of_dicts)