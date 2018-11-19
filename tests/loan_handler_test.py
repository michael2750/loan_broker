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
		self.body = [
			{
				'ssn': 160578987,
				'credit_score': 598,
				'loan_amount': 1000000, 
				'loan_duration': 360
			}
		]

	def test_handle_request(self):
		print("testing handle_request")
		json_string = json.dumps(self.body)
		result = handle_request(json_string)
		assert test_id is not None

	def test_handle_result(self):
		pass

if __name__ == '__main__':
	unittest.main()