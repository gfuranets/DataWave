import sys
import unittest
from datetime import datetime, timezone
from pathlib import Path

from jose import jwt

APP_DIR = Path(__file__).resolve().parents[1] / "app"
sys.path.insert(0, str(APP_DIR))

from auth import ALGORITHM, SECRET_KEY, create_access_token


class TokenuIzsniegsanaTests(unittest.TestCase):
    def test_tokenu_izsniegsana(self):
        token = create_access_token({"sub": "1"})

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        self.assertEqual(payload["sub"], "1")
        self.assertIn("iat", payload)
        self.assertIn("exp", payload)
        self.assertGreater(
            datetime.fromtimestamp(payload["exp"], timezone.utc),
            datetime.now(timezone.utc),
        )


if __name__ == "__main__":
    unittest.main()
