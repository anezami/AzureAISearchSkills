import json
import unittest
from unittest.mock import MagicMock
from address_merge_skill import main

class TestAddressMergeSkill(unittest.TestCase):
    def test_address_merge(self):
        # Test sample data
        test_request_body = {
            "values": [
                {
                    "recordId": "1",
                    "data": {
                        "streetName": "Main Street",
                        "houseNumber": "123B",
                        "city": "New York"
                    }
                },
                {
                    "recordId": "2",
                    "data": {
                        "streetName": "Park Avenue",
                        "houseNumber": "456 33B",
                        "city": "San Francisco"
                    }
                }
            ]
        }
        
        # Create mock request
        req_body = json.dumps(test_request_body).encode()
        req = MagicMock(spec=func.HttpRequest)
        req.get_json.return_value = test_request_body
        req.get_body.return_value = req_body
        
        # Call the function
        response = main(req)
        
        # Parse the response
        response_body = json.loads(response.get_body())
        results = response_body.get('values', [])
        
        # Verify the results
        self.assertEqual(len(results), 2)
        
        # Check first record
        self.assertEqual(results[0]['recordId'], '1')
        self.assertEqual(results[0]['data']['fullAddress'], 'Main Street 123B, New York')
        
        # Check second record
        self.assertEqual(results[1]['recordId'], '2')
        self.assertEqual(results[1]['data']['fullAddress'], 'Park Avenue 456 33B, San Francisco')

        print("Response:", results[0]['data']['fullAddress'])
        print("Response:", results[1]['data']['fullAddress'])

if __name__ == '__main__':
    unittest.main()