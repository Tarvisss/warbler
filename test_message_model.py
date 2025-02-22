import os
from unittest import TestCase
from sqlalchemy import exc

from models import db, User, Message, Follows, Likes

os.environ['DATABASE_URL'] = "postgresql: ///warbler-test"


from app import app


db.create_all()


class UserModelTestCase(TestCase):
    """ let's test views for messages"""

    def setUp(self):

        db.drop_all()
        db.create_all()

        self.uid = 85342
        u = User.signup("yo this is a test", "myemail@gmail.com", "mypassord", None)

        u.id = self.uid
        db.session.commit()

        self.u = User.query.get(self.uid)

        self.client = app.test_client()


    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res

    def test_message_model(self):
        """Does basic model work?"""
        
        m = Message(
            text="a warble",
            user_id=self.uid
        )

        db.session.add(m)
        db.session.commit()

        # User should have 1 message
        self.assertEqual(len(self.u.messages), 1)
        self.assertEqual(self.u.messages[0].text, "a warble")

    def test_message_likes(self):
        m1 = Message(
            text="wallow in self pity",
            user_id=self.uid
        )

        m2 = Message(
            text="my life sucks ",
            user_id=self.uid 
        )

        user = User.signup("Testing1234", "awesome@email.com", "tiredofthis", None)
        uid = 888
        user.id = uid
        db.session.add_all([m1, m2, user])
        db.session.commit()

        user.likes.append(m1)

        db.session.commit()

        l = Likes.query.filter(Likes.user_id == uid).all()
        self.assertEqual(len(l), 1)
        self.assertEqual(l[0].message_id, m1.id)