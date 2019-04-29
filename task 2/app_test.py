
# todo add to reqs
import unittest
from httplib import responses

import requests


class ApiTest(unittest.TestCase):

    def test_post_requests(self):
        # self.assertEqual(requests.post('http://localhost:5000/', json={"mytext":"lalala"}), responses.pos)
        print(requests.get('http://localhost:5000/').json())
