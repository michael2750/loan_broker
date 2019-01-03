import pika
import json
from sql_statements import insert_result
from threading import Thread
import datetime
import time

list_of_dicts = []

def commit():
	global list_of_dicts
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

def thread_method(threadname):
	connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
	channel = connection.channel()

	channel.queue_declare(queue='aggregator')

	def callback(ch, method, properties, body):
		global list_of_dicts
		print(body)
		json_string = json.loads(body)
		list_of_dicts.append(json_string)
		if len(list_of_dicts) == 4:
			temp_list = list_of_dicts
			#list_of_dicts = []
			commit()
			

	channel.basic_consume(callback,
	                      queue='aggregator',
	                      no_ack=True)

	print(' [*] Waiting for messages. To exit press CTRL+C')
	channel.start_consuming()



def monitor(threadname, ssn_dict):
	global list_of_dicts
	while True:
		print(len(list_of_dicts))
		if len(list_of_dicts) > 0:
			for bank_dict in list_of_dicts:
				for x, y in bank_dict.items():
					if y["ssn"] not in ssn_dict:
						ssn_dict[y["ssn"]] = datetime.datetime.now()
		for x,y in ssn_dict.items():
			time_stamp = datetime.datetime.now()
			diff = (time_stamp - y).total_seconds()
			if diff > 2:
				temp_list = list_of_dicts
				#list_of_dict = []
				ssn_dict = {}
				commit()
		time.sleep(0.5)
ssn_dict = {}

thread_1 = Thread(target=thread_method, args=('thread_1',))
thread_2 = Thread(target=monitor, args=('thread_2',  ssn_dict))
thread_1.start()
thread_2.start()
thread_1.join()
thread_2.join()
