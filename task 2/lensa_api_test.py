import unittest
import requests
from werkzeug import exceptions
import os
import json
from lensa_api import app

testapp = app.test_client()
app.testing = True

BACKUP_FILE = "backup.json"
FIRST_ITEM = "first"
SECOND_ITEM = "second"
TEST_DATA_0 = {
    "item": FIRST_ITEM
}

TEST_DATA_1 = {
    "item": SECOND_ITEM
}

INT_DATA = 2
TEST_DATA_INT = {
    "item": INT_DATA
}


class TestFlaskApi(unittest.TestCase):

    def setUp(self):
        self._delete_backup_file()
        self._create_backup_file()

    def test_fresh_start(self):
        self.assertEqual(self._get_data(), [])

    def test_post_request(self):
        self._successful_post_request(TEST_DATA_0)
        response = requests.get('http://localhost:5000')
        self.assertEqual(response.json(), [FIRST_ITEM])

        self._successful_post_request(TEST_DATA_1)
        response = requests.get('http://localhost:5000')
        self.assertEqual(response.json(), [FIRST_ITEM, SECOND_ITEM])

        self._successful_post_request(TEST_DATA_INT)

    def test_duplicated_data(self):
        self._delete_backup_file()
        self._create_backup_file()

        response = testapp.post("/", json=TEST_DATA_0)
        self.assertEqual(f"{TEST_DATA_0['item']} inserted to database.", response.get_data().decode("utf-8"))
        self.assertEqual(200, response.status_code)

        response = testapp.post("/", json=TEST_DATA_0)
        self.assertEqual(f"'{FIRST_ITEM}' is already in DB.", response.get_data().decode("utf-8"))
        self.assertEqual(exceptions.Conflict.code, response.status_code)

        response = testapp.post("/", json=TEST_DATA_0)
        self.assertEqual(f"'{FIRST_ITEM}' is already in DB.", response.get_data().decode("utf-8"))
        self.assertEqual(exceptions.Conflict.code, response.status_code)

    def test_put_request(self):
        response = testapp.put("/", data=TEST_DATA_0)
        self.assertEqual(exceptions.MethodNotAllowed.code, response.status_code)

    def test_delete_request(self):
        response = testapp.delete("/", data=TEST_DATA_0)
        self.assertEqual(exceptions.MethodNotAllowed.code, response.status_code)

    def tearDown(self):
        self._delete_backup_file()

    def _create_backup_file(self):
        try:
            with open(BACKUP_FILE, "r") as backup_file:
                _ = backup_file.readlines()
        except FileNotFoundError:
            with open(BACKUP_FILE, "w") as backup_file:
                json.dump({"items": []}, backup_file)

    def _get_data(self):
        return requests.get('http://localhost:5000').json()

    def _delete_backup_file(self):
        try:
            path = os.path.join(os.getcwd(), BACKUP_FILE)
            os.remove(path)
        except FileNotFoundError:
            pass

    def _successful_post_request(self, test_data):
        response = testapp.post("/", json=test_data)
        self.assertEqual(200, response.status_code)
        self.assertEqual(f"{test_data['item']} inserted to database.", response.get_data().decode("utf-8"))



if __name__ == "__main__":
    unittest.main()
