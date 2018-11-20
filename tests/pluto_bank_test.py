import pika
import unittest
import json
import os, sys
from unittest.mock import patch
parentPath = os.path.abspath("../")
if parentPath not in sys.path:
    sys.path.insert(0,parentPath)
from pluto_bank import handle_callback_body

class TestPlutoBank(unittest.TestCase):

    def setUp(self):
        self.body = {
            'ssn': '160578-9871',
            'credit_score': 598,
            'loan_amount': 1000000, 
            'loan_duration': 360
        }

    def test_get_ssn(self):
        print("testing handle_callback_body_ssn")
        json_string = json.dumps(self.body)
        self.result = handle_callback_body(json_string)
        self.result = json.loads(self.result)
        self.assertEqual(self.result['ssn'], 160578987)

    def test_get_interest_rate(self):
        print("testing handle_callback_body_interest_rate")
        json_string = json.dumps(self.body)
        self.result = handle_callback_body(json_string)
        self.result = json.loads(self.result)
        self.assertEqual(self.result['interest'], 3.5)

if __name__ == '__main__':
    unittest.main()