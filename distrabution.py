import pika
import requests
import json
import datetime

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()


channel.queue_declare(queue='distrabution')


'''
def bankXML(json_string):
	ssn = json_string["ssn"].replace("-","")[:-2]
	cs = json_string["credit_score"]
	loan_amount = json_string["loan_amount"]
	duration = (datetime.datetime.now() + datetime.timedelta(days=json_string["loan_duration"])).strftime("%Y-%m-%d %H:%M:%S")
	fibonacci_rpc = BankXML()
	response = fibonacci_rpc.call(f"""<LoanRequest>
							<ssn>{ssn}</ssn>
							<creditScore>{cs}</creditScore>
							<loanAmount>{loan_amount}</loanAmount>
							<loanDuration>{duration}.0 CET</loanDuration>
							</LoanRequest>""")
	print(" BANKXML [.] Got %r" % response)

# 1973-01-01 01:00:00.0 CET

def pluto_bank(json_string):
    pluto_bank = PlutoBank()
    response = pluto_bank.call(json_string)
    print(" PLUTOBANK [.] Got %r" % response)

def bank_json(json_string):
    new_json_string = {}
    new_json_string["ssn"] = json_string["ssn"].replace("-","")
    new_json_string["loanAmount"] = float(json_string["loan_amount"])
    new_json_string["loanDuration"] = json_string["loan_duration"]
    #new_json_string["rki"] = False
    bank_json = BankJSON()
    response = bank_json.call(new_json_string)
    print(" BANKJSON [.] Got %r" % response)

'''

# {"ssn":1605789787,"loanAmount":10.0,"loanDuration":360,"rki":false}

def callback(ch, method, properties, body):
    global channel
    json_string = json.loads(body)
    print(json.dumps(json_string))
    count = 1
    print(len(json_string["banks"]))
    for bank in json_string["banks"]:
        if bank == "Amagerbanken":
            r = requests.post(url = "http://159.65.116.24:5000/request", json = json_string)
            print(r.body)
        if bank == "Nordea":
            channel.basic_publish(exchange='',
                          routing_key='bank_pluto_translator',
                          body=json.dumps(json_string))
        if bank == "Banknordic":
            channel.basic_publish(exchange='',
                          routing_key='bankXML_translator',
                          body=json.dumps(json_string))
        if bank == "Danskebank":
            channel.basic_publish(exchange='',
                          routing_key='bankJSON_translator',
                          body=json.dumps(json_string))

        print(count)
        count += 1


channel.basic_consume(callback,
                      queue='distrabution',
                      no_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()