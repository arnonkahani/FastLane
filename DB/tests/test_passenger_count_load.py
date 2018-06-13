import unittest

from sqlalchemy_utils import drop_database

from DB.db.managers.passenger_count_db import PassengerCountDB
from DB.db.model.passenger_count import PassengerCount
from DB.tests.test_utils import create_test_db_with_schemas, create_session


class PassengerCountTest(unittest.TestCase):
    def setUp(self):
        self.config, self.engine,self.dm_manager = create_test_db_with_schemas()
        self.config.SHOULD_PASSENGER_LOAD_DATA = True

    def test_passenger_count_load(self):

        passenger_count_db = PassengerCountDB(self.dm_manager.db,self.config)
        passenger_count_db.load_data()
        session = create_session(self.engine)
        passenger_count_select_all = list(session.query(PassengerCount))
        self.assertEqual(len(passenger_count_select_all), 109,
                         'the passenger count table size in the db don\'t match the raw data file size')

    def tearDown(self):
        drop_database(self.engine.url)
