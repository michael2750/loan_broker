import unittest
import json
import pika
import os, sys
from unittest.mock import patch
parentPath = os.path.abspath("../")
if parentPath not in sys.path:
    sys.path.insert(0,parentPath)
from loan_handler import handle_request, handle_result

class TestLoanHandler (unittest.TestCase):

	def setUp(self):
		self.body = {
			'ssn': '160578-9872',
			'loan_amount': 1000000, 
			'loan_duration': 360
		}

		self.json_string = json.dumps(self.body)
		self.json_string = json.loads(self.json_string)
		self.test_id = handle_request(self.json_string)
		self.interest_result = handle_result(self.test_id)

	def test_handle_request(self):
		print("---testing handle_request---")
		self.result = self.test_id
		assert self.result is not None

	def test_handle_result_under_progress(self):
		print("---testing handle_result_under_progress---")
		self.assertEqual(self.interest_result, "under progress")

	def test_handle_result_interest_rate(self):
		print ("---testing handle_result_interest_rate---")
		self.result = json.loads(self.interest_result)
		assert self.result['interest'] is not None

if __name__ == '__main__':
	unittest.main()