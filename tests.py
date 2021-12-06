from unittest import TestCase
from server import app
from model import connect_to_db, db, example_data
from flask import session
from werkzeug.security import (generate_password_hash, check_password_hash)



class FlaskTestsBasic(TestCase):
    """Flask tests."""

    def setUp(self):
        """Set up."""

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True
        connect_to_db(app, "postgresql:///testdb")
        app.config['SECRET_KEY'] = 'plantsarethebest'
        # Get the Flask test client
        self.client = app.test_client()
        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 1
   
        db.create_all()
        example_data() 

    def test_homepage(self):
        """Test homepage page."""

        result = self.client.get("/")
        self.assertIn(b"Welcome to", result.data)

    def test_login(self):
        """Test login page."""

        result = self.client.post("/login",
                                  data={"email": "user1@test.com", "password": "testing"},
                                  follow_redirects=True)
        self.assertIn(b"Plant Search", result.data)

    def test_all_plants(self):
        """Test all plants."""

        result = self.client.get("/plants")
        self.assertIn(b"All Plants", result.data)
        self.assertIn(b"Aloe Vera", result.data)
    
    def test_user_plants(self):
        """Test all User Plants."""

        result = self.client.get("/user_plants/2",)                          
        self.assertIn(b"Plant Tracker", result.data)
        self.assertIn(b"full sun", result.data)
       
    def test_user_password_hash(self):
        """Test all hashed passwords."""

        real_password = "Test@123!"
        hash_password = generate_password_hash("Test@123!", method='sha256')

        # generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)
        # The crux of each test is a call to assertEqual() to check for an expected result;
        # assertTrue() or assertFalse() to verify a condition
      
        
        result = check_password_hash(hash_password, real_password)
        self.assertTrue(result)

    def tearDown(self): 
        """Drop data at end of every test."""

        db.session.remove()
        db.drop_all()
        db.engine.dispose()

if __name__ == "__main__":
    import unittest
    unittest.main()