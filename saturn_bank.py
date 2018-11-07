from flask import Flask
from flask import request
from flask import render_template
import json
import requests
import logging


app = Flask(__name__)


body = [
    {
        'ssn': 160578987,
        'creditScore': 598,
        'loanAmount': 1000000, 
        'loanDuration': 360
    }
]


@app.route('/request', methods=['POST'])
def request():
	json_string = request.get_json()
	ssn = json_string['ssn']
	interest_rate = calc_interest_rate(json_string)
	data = {'ssn': ssn, 'interest_rate': interest_rate}
	return data


def calc_interest_rate(body):
	data = json.loads(body)
	credit_score = data['creditScore']
	loan_amount = data['loanAmount']
	loan_duration = data['loanDuration']
	print(data)
	if loan_amount > 1000000:
		interest_rate = 1
	else:
		interest_rate = 3
	return interest_rate


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0", port=5000)