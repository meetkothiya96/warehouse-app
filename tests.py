import unittest
from app import app, db  # <--- Import 'db' here

class BasicTests(unittest.TestCase):
    def setUp(self):
        # Create a test client
        self.app = app.test_client()
        self.app.testing = True

        # --- THE FIX STARTS HERE ---
        # We must manually create the tables inside the test environment
        with app.app_context():
            db.create_all()
        # --- THE FIX ENDS HERE ---

    def test_home_page(self):
        # Send a GET request to '/'
        response = self.app.get('/')
        # Check if the page loads (Status 200)
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()