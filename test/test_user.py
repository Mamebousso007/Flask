# import unittest
# from app import create_app, db
# from config import TestingConfig

# class UserModelTestCase(unittest.TestCase):

#     @classmethod
#     def setUpClass(cls):
#         # Crée une instance de l'application avec la configuration de test
#         cls.app = create_app(TestingConfig)
#         cls.app_context = cls.app.app_context()
#         cls.app_context.push()
#         db.create_all()  # Crée les tables de la base de données de test

#     @classmethod
#     def tearDownClass(cls):
#         db.session.remove()
#         db.drop_all()  # Supprime les tables de la base de données de test
#         cls.app_context.pop()

#     def test_user_registration(self):
#         with self.app.test_client() as client:
#             response = client.post('/api/auth/register', json={
#                 'username': 'testuser',
#                 'email': 'testuser@example.com',
#                 'password': 'testpassword',
#                 'role': 'USER'
#             })
#             self.assertEqual(response.status_code, 201)
#             self.assertIn(b'User registered successfully', response.data)

#     def test_user_login(self):
#         with self.app.test_client() as client:
#             # Enregistrement d'un utilisateur avant de tester la connexion
#             client.post('/api/auth/register', json={
#                 'username': 'testuser',
#                 'email': 'testuser@example.com',
#                 'password': 'testpassword',
#                 'role': 'USER'
#             })
#             response = client.post('/api/auth/login', json={
#                 'email': 'testuser@example.com',
#                 'password': 'testpassword'
#             })
#             self.assertEqual(response.status_code, 200)
#             self.assertIn(b'token', response.data)

# if __name__ == '__main__':
#     unittest.main()
