import unittest
from fastapi.testclient import TestClient

from src.app import app


class AdminModeTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_admin_me_is_none_without_login(self):
        response = self.client.get('/admin/me')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'username': None})

    def test_teacher_login_sets_cookie(self):
        response = self.client.post('/admin/login', params={'username': 'admin', 'password': 'admin'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('teacher_session', response.cookies)

    def test_student_signup_requires_teacher_login(self):
        response = self.client.post('/activities/Chess Club/signup', params={'email': 'newstudent@mergington.edu'})
        self.assertEqual(response.status_code, 403)
        self.assertIn('Teacher login required', response.json()['detail'])

    def test_teacher_can_sign_up_student(self):
        with self.client as client:
            login = client.post('/admin/login', params={'username': 'admin', 'password': 'admin'})
            self.assertEqual(login.status_code, 200)

            response = client.post('/activities/Chess Club/signup', params={'email': 'teacherstudent@mergington.edu'})
            self.assertEqual(response.status_code, 200)
            self.assertIn('teacherstudent@mergington.edu', client.get('/activities').json()['Chess Club']['participants'])


if __name__ == '__main__':
    unittest.main()
