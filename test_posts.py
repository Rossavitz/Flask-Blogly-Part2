from unittest import TestCase

from app import app
from models import db, Post, User

# use test database and dont clutter tests with sql
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///blogly_test"
app.config["SQLALCHEMY_ECHO"] = False

# make flask errors be real errors rather than html pages with error info
app.config["TESTING"] = True

# this is a bit of a hack, but dont use flask debugtoolbar
app.config["DEBUT_TB_HOSTS"] = ["dont-show-debug-toolbar"]

db.drop_all()
db.create_all()


class PostViewsTestCase(TestCase):
    """testing for posts"""

    def setUp(self):
        """add a sample user and post"""

        # User.query.delete()
        # Post.query.delete()

        user = User(first_name="Test", last_name="Case")
        db.session.add(user)
        db.session.commit()
        self.user_id = user.id

        post = Post(title="Test title", content="Test Content", user_id="1")
        db.session.add(post)
        db.session.commit()
        self.post_id = post.id

    def tearDown(self):
        """clean up any fouled transaction"""

        db.session.rollback()

    def test_show_post(self):
        with app.test_client() as client:
            resp = client.get(f"/posts/1")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Test title", html)

    def test_add_post(self):
        with app.test_client() as client:
            d = {"title": "Test2", "content": "Test Content 2"}
            resp = client.post(
                f"/users/{self.user_id}/posts/new", data=d, follow_redirects=True
            )
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Test2", html)

    def test_delete_post(self):
        with app.test_client() as client:
            resp = client.post(f"/posts/{self.post_id}/delete", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn("Test title", html)
