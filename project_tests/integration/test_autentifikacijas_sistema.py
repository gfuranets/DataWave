import warnings

warnings.simplefilter("ignore")

from tests.helpers import FastAPIIntegrationTestCase

import models
from auth import verify_password


class AutentifikacijasSistemaTests(FastAPIIntegrationTestCase):
    def test_signup_login_data_logout_flow(self):
        username = "integration_user"
        password = "integration_password"

        signup_page = self.client.get("/signup")
        self.assertEqual(signup_page.status_code, 200)
        self.assertIn("Signup", signup_page.text)

        signup_response = self.client.post_form(
            "/signup",
            {"username": username, "password": password},
        )
        self.assertEqual(signup_response.status_code, 200)

        db = self.SessionLocal()
        try:
            user = db.query(models.User).filter(models.User.username == username).first()
            self.assertIsNotNone(user)
            self.assertTrue(verify_password(password, user.password))
        finally:
            db.close()

        login_response = self.client.post_form(
            "/login",
            {"username": username, "password": password},
        )
        self.assertEqual(login_response.status_code, 200)
        self.assertIn("access_token", self.client.cookies)

        data_page = self.client.get("/data")
        self.assertEqual(data_page.status_code, 200)
        self.assertIn("Data", data_page.text)
        self.assertIn(username, data_page.text)

        logout_response = self.client.get("/logout")
        self.assertEqual(logout_response.status_code, 200)

        protected_page = self.client.get("/data", follow_redirects=False)
        self.assertEqual(protected_page.status_code, 401)
