from flask import Flask
from flask import request
from flask import render_template
import json

app = Flask(__name__)

@app.route('/request', methods=['POST'])
def get_request():
	json_string = request.get_json()
	data = handle_request(json_string)
	return json.dumps(data)

def handle_request(body):
	body = json.loads(body)
	interest_rate = calc_interest_rate(body)
	ssn = body['ssn']
	data = {'ssn': ssn, 'interest_rate': interest_rate}
	json_string = json.dumps(data)
	return json_string

def calc_interest_rate(body):
	credit_score = body['credit_score']
	loan_amount = body['loan_amount']
	loan_duration = body['loan_duration']
	if loan_amount > 1000000:
		interest_rate = 1
	else:
		interest_rate = 3
	return interest_rate

if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0", port=5000)
