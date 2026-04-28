import sys
import unittest
from pathlib import Path

APP_DIR = Path(__file__).resolve().parents[1] / "app"
sys.path.insert(0, str(APP_DIR))

from auth import PASSWORD_HASH_PREFIX, hash_password, verify_password


class ParolesHashesanaTests(unittest.TestCase):
    def test_paroles_hashesana(self):
        password = "mana-drosa-parole"

        hashed = hash_password(password)

        self.assertNotEqual(hashed, password)
        self.assertTrue(hashed.startswith(PASSWORD_HASH_PREFIX))
        self.assertTrue(verify_password(password, hashed))
        self.assertFalse(verify_password("nepareiza-parole", hashed))

    def test_paroles_hashesana_garam_parolem(self):
        password = "a" * 200

        hashed = hash_password(password)

        self.assertTrue(verify_password(password, hashed))


if __name__ == "__main__":
    unittest.main()
