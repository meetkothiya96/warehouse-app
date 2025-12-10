import unittest
from app import app

class BasicTests(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        
    def test_home_page(self):
        response = self.app.get('/')
        self.assertTrue(response.status_code in [200, 302])


if __name__ == "__main__":
    unittest.main()