from flask import Flask
from flask import request
from sql_statements import insert_request, select_result
import pika
import json

app = Flask(__name__)

@app.route('/request', methods=['POST'])
def get_request():
	json_string = request.get_json()
	ssn = json_string['ssn']
	loan_amount = json_string['loan_amount']
	loan_duration = json_string['loan_duration']
	request_id = insert_request(ssn, loan_amount, loan_duration)
	start_process(ssn, loan_amount, loan_duration)
	return str(request_id)

@app.route('/result', methods=['GET'])
def get_result():
	request_id = request.args.get('request_id')
	result = select_result(request_id)
	if result['interest']:
		return json.dumps(result)
	else:
		return "under progress"

def start_process(ssn, loan_amount, loan_duration):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    body = {"ssn": ssn, "loan_amount": loan_amount, "loan_duration": loan_duration}
    channel.basic_publish(exchange='',
                          routing_key='credit_score',
                          body=json.dumps(body))
    connection.close()

if __name__ == '__main__':
	app.run(debug=True,host="0.0.0.0", port=5003)
