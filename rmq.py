#!/usr/bin/env python
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='datdb.cphbusiness.dk', port='5672'))
channel = connection.channel()


queue = channel.queue_declare().method.queue

def on_response(ch, method, props, body):
    print(" [x] Received %r" % body)


channel.basic_publish(exchange='cphbusiness.bankXML',
                      routing_key='',
                      body="""<LoanRequest>
<ssn>12345678</ssn>
<creditScore>685</creditScore>
<loanAmount>1000.0</loanAmount>
<loanDuration>1973-01-01 01:00:00.0 CET</loanDuration>
</LoanRequest>""")

#channel.basic_consume(callback,
#                      queue=queue,
#                      no_ack=True)

#channel.start_consuming()

print("test")

connection.close()
