import pika
import json
from sql_statements import insert_result

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()


channel.queue_declare(queue='aggregator')

def callback(ch, method, properties, body):
	print(body)



channel.basic_consume(callback,
                      queue='aggregator',
                      no_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()