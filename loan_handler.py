from flask import Flask
from flask import request
from sql_statements import insert_request, select_result

app = Flask(__name__)

@app.route('/request', methods=['POST'])
def get_request():
	json_string = request.get_json()
	ssn = json_string['ssn']
	loan_amount = json_string['loanAmount']
	loan_duration = json_string['loanDuration']
	request_id = insert_request(ssn, loan_amount, loan_duration)
	return str(request_id)

@app.route('/result', methods=['GET'])
def get_result():
	request_id = request.args.get('request_id')
	result = select_result(request_id)
	if result['interest']:
		return json.dumps(result)
	else:
		return "under progress"

if __name__ == '__main__':
	app.run(debug=True,host="0.0.0.0", port=5004)