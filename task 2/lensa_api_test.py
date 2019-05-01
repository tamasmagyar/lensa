import unittest
import requests
from flask import jsonify
from lensa_api import app

testapp = app.test_client()
app.testing = True


class TestFlaskApi(unittest.TestCase):

    def test_clean_api(self):
        response = requests.get('http://localhost:5000')
        self.assertEqual(response.json(), [])

    def test_post_api(self):
        with testapp as client:
            data = jsonify({"item": "beer"})
            response = client.post("/", data)
            # response = requests.post('http://localhost:5000', data)
            self.assertEqual(response.json(), "beer is inserted to db.")


if __name__ == "__main__":
    unittest.main()
