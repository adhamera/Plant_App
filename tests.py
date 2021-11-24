from unittest import TestCase
from server import app
from model import connect_to_db, db, example_data
from flask import session



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
        self.assertIn(b"Welcome to Plantlet!", result.data)

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
       


    def tearDown(self): 
        """Drop data at end of every test."""

        db.session.remove()
        db.drop_all()
        db.engine.dispose()

if __name__ == "__main__":
    import unittest
    unittest.main()