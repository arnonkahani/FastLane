import unittest

from sqlalchemy_utils import drop_database

from DB.db.managers.gtfs_db import GTFSDB
from DB.db import Stop, StopTime, Trip, Calendar, Pattern, Route, Agency
from DB.tests.test_utils import create_test_db_with_schemas, create_session


class GTFSLoadTest(unittest.TestCase):
    def setUp(self):
        self.config, self.engine, self.dm_manager = create_test_db_with_schemas()
        self.config.SHOULD_LOAD_GTFS_DATA = True

    def test_gtfs_load(self):
        gtfs_db = GTFSDB(self.dm_manager.db, self.config)
        gtfs_db.load_data()
        session = create_session(self.engine)
        stop_select_all = list(session.query(Stop))
        stop_time_select_all = list(session.query(StopTime))
        agency_select_all = list(session.query(Agency))
        trip_select_all = list(session.query(Trip))
        calendar_select_all = list(session.query(Calendar))
        pattren_select_all = list(session.query(Pattern))
        route_select_all = list(session.query(Route))
        tables = [stop_select_all, stop_time_select_all, trip_select_all, route_select_all, calendar_select_all,
                  agency_select_all, pattren_select_all]

        stop_len = 33035
        stop_time_len = 185953
        trip_len = 6929
        route_len = 70
        calendar_len = 192649
        agency_len = 19
        pattren_len = 69

        ground_truth_lengths = [stop_len, stop_time_len, trip_len, route_len, calendar_len, agency_len,
                                pattren_len]
        tables_lengths = list(map(lambda table: len(table), tables))

        self.assertEqual(ground_truth_lengths, tables_lengths,
                         'the gtfs count table size in the db don\'t match the raw data file size')

    def tearDown(self):
        drop_database(self.engine.url)
