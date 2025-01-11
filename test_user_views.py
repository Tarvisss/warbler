import os
from unittest import TestCase
from sqlalchemy import exc
from bs4 import BeautifulSoup
from models import db, User, Message, Follows, Likes, connect_db

os.environ['DATABASE_URL'] = "postgresql: ///warbler-test"

from app import app, CURR_USER_KEY

db.create_all()
app.config['WTF_ENABLED'] = False

class MessageViewTestCase(TestCase):
    """Test views for messages"""


    def setUp(self):
        """create sample data for a test client"""

        db.drop_all()
        db.create_all()

        self.client = app.test_client()

        self.testuser = User.signup(username="testuser",
                                    email = "test@test.com",
                                    password = "testuser",
                                    image_url= None)
        
        self.testuser_id = 9000
        self.testuser.id = self.testuser_id

        self.u1 = User.signup("abc","test0@test.com", "password", None)
        self.u1_id = 900
        self.u1.id = self.u1_id




        db.session.commit()

    def tearDown(self):
        resp = super().tearDown()
        db.session.rollback()
        return resp

    def test_users_index(self):
        with self.client as c:
            resp = c.get("/users")

            
            self.assertIn("@abc", str(resp.data))
           
    def test_user_show(self):
        with self.client as c:
            resp = c.get(f"/users/{self.testuser_id}")

            self.assertEqual(resp.status_code, 200)

            self.assertIn("@testuser", str(resp.data))

    def test_user_show_with_likes(self):
        self.setup_likes()

        with self.client as c:
            resp = c.get(f"/users/{self.testuser_id}")

            self.assertEqual(resp.status_code, 200)

            self.assertIn("@testuser", str(resp.data))
            soup = BeautifulSoup(str(resp.data), 'html.parser')
            found = soup.find_all("li", {"class": "stat"})
            self.assertEqual(len(found), 4)

            # test for a count of 2 messages
            self.assertIn("2", found[0].text)