from tests.helpers import DatabaseTestCase

import crud
import models
from auth import verify_password


class LietotajaIzveideTests(DatabaseTestCase):
    def test_lietotaja_izveide(self):
        crud.signup("artur", "parole123", self.db)

        user = self.db.query(models.User).filter(models.User.username == "artur").first()

        self.assertIsNotNone(user)
        self.assertEqual(user.username, "artur")
        self.assertNotEqual(user.password, "parole123")
        self.assertTrue(verify_password("parole123", user.password))
