# from app import app, db, Users, bcrypt, current_user
# from flask_testing import TestCase
# import unittest
# import os
#
#
# class BaseTestCase(TestCase):
#     def create_app(self):
#         app.config['DEBUG'] = True
#         app.config['Testing'] = True
#         app.config['WTF_CSRF_ENABLED'] = False
#         app.config['SECRET_KEY'] = str(os.environ.get("FLASK_SECRET_KEY"))
#         app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
#         return app
#
#     def setUp(self):
#         db.create_all()
#         db.session.add(Users(username="test", password="$2y$12$lcYrKeAkB5b7dYRep1Yj6etbkmfqGXONkWrFVbs6rVcIOm6KN.1lC",
#                              admin_role=True))
#
#     def tearDown(self):
#         db.session.remove()
#         db.drop_all()
#
#
# class FlaskTestCase(BaseTestCase):
#     def test_index(self):
#         response = self.client.get('/', content_type='html/text')
#         self.assertEqual(response.status_code, 200)
#
#     def test_login_page_loads(self):
#         response = self.client.get('/', content_type='html/text')
#         self.assertTrue(b'Username' in response.data)
#
#     def test_corect_login(self):
#         with self.client:
#             response = self.client.post(
#                 '/',
#                 data=dict(username="test", password="test"),
#                 follow_redirects=True
#             )
#             self.assertIn(b'Switch intervals on/off', response.data)
#             self.assertTrue(current_user.username == "test")
#             self.assertTrue(current_user.is_active)
#
#     def test_incorect_login(self):
#         response = self.client.post(
#             '/',
#             data=dict(username="test", password="wrongPassword"),
#             follow_redirects=True
#         )
#         self.assertIn(b'Wrong credentials!', response.data)
#
#     def test_logout(self):
#         with self.client:
#             response = self.client.post(
#                 '/',
#                 data=dict(username="test", password="test"),
#                 follow_redirects=True
#             )
#             response = self.client.get('/logout', follow_redirects=True)
#             self.assertIn(b'Username', response.data)
#             self.assertFalse(current_user.is_active)
#
#     def test_the_login_is_required(self):
#         response = self.client.get('/room', follow_redirects=True)
#         self.assertTrue(b'Unauthorized' in response.data)
#
#     def test_password_hashing(self):
#         user = Users.query.filter_by(username="test").first()
#         self.assertTrue(bcrypt.check_password_hash(user.password, 'test'))
#         self.assertFalse(bcrypt.check_password_hash(user.password, 'wrongPassword'))
#
#
# if __name__ == '__main__':
#     unittest.main()
