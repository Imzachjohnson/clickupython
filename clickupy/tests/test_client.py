# tests/tests_clickup.py
import unittest
import client

class TestClient(unittest.TestCase):
    def test_get_list(self):
        result = client.client.get_list
        self.assert