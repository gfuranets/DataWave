from tests.helpers import DatabaseTestCase

import crud
import models


class KugaPievienosanaTests(DatabaseTestCase):
    def test_kuga_pievienosana(self):
        crud.signup("artur", "parole123", self.db)
        user = self.db.query(models.User).filter(models.User.username == "artur").first()

        crud.create_ship(user.user_id, "Wave 1", self.db)

        ship = self.db.query(models.Ship).filter(models.Ship.name == "Wave 1").first()
        self.assertIsNotNone(ship)
        self.assertEqual(ship.user_id_refer, user.user_id)
