from datetime import datetime, timedelta

from tests.helpers import DatabaseTestCase

import crud
import models


class StatistikasApskateTests(DatabaseTestCase):
    def test_statistikas_apskate_kugim_laika_perioda(self):
        crud.signup("artur", "parole123", self.db)
        user = self.db.query(models.User).filter(models.User.username == "artur").first()
        crud.create_ship(user.user_id, "Wave 1", self.db)
        crud.create_ship(user.user_id, "Wave 2", self.db)
        ship = self.db.query(models.Ship).filter(models.Ship.name == "Wave 1").first()
        other_ship = self.db.query(models.Ship).filter(models.Ship.name == "Wave 2").first()
        now = datetime.now()

        crud.post_data(ship.ship_id, "temp=20", now - timedelta(minutes=10), self.db)
        crud.post_data(ship.ship_id, "temp=21", now, self.db)
        crud.post_data(other_ship.ship_id, "temp=99", now, self.db)

        measurements = (
            self.db.query(models.Data)
            .filter(models.Data.ship_id_refer == ship.ship_id)
            .filter(models.Data.timestamp >= now - timedelta(hours=1))
            .order_by(models.Data.timestamp)
            .all()
        )

        self.assertEqual([row.data for row in measurements], ["temp=20", "temp=21"])
