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
			'ssn': 160578987,
			'loan_amount': 1000000, 
			'loan_duration': 360
		}
		
		json_string = json.dumps(self.body)
		self.test_id = handle_request(json_string)

	def test_handle_request(self):
		print("---testing handle_request---")
		result = self.test_id
		assert result is not None

	def test_handle_result_under_progress(self):
		print("---testing handle_result_under_progress---")
		result = handle_result(self.test_id)
		self.assertEquals(result, "under progress")

	def test_handle_result_interest_rate(self):
		print ("---testing handle_result_interest_rate---")
		result = handle_result(self.test_id)
		result = json.loads(result)
		#assert result['interest_rate'] is not None
		pass

if __name__ == '__main__':
	unittest.main()