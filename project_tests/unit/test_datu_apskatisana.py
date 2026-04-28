from datetime import datetime

from tests.helpers import DatabaseTestCase

import crud
import models


class DatuApskatisanaTests(DatabaseTestCase):
    def test_datu_apskatisana(self):
        crud.signup("artur", "parole123", self.db)
        user = self.db.query(models.User).filter(models.User.username == "artur").first()
        crud.create_ship(user.user_id, "Wave 1", self.db)
        ship = self.db.query(models.Ship).filter(models.Ship.name == "Wave 1").first()

        crud.post_data(ship.ship_id, "temp=20;pressure=1010", datetime.now(), self.db)

        data_rows = self.db.query(models.Data).all()
        self.assertEqual(len(data_rows), 1)
        self.assertEqual(data_rows[0].ship_id_refer, ship.ship_id)
        self.assertEqual(data_rows[0].data, "temp=20;pressure=1010")
