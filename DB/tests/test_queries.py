import pickle
import unittest

from sqlalchemy_utils import drop_database

from DB.queries import query_trips_info_by_area, query_stops_info_by_path, query_stoptimes_info_by_area, \
    query_stoptimes_info_by_path, get_trips_info_by_area, get_stoptimes_info_by_path, get_v_info_by_path, \
    get_stoptimes_info_by_area
from DB.tests.test_utils import create_gtfs_db


class GTFSLoadTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config, cls.engine, cls.db_manager, cls.session = create_gtfs_db()

    def test_query_trips_info_by_area(self):
        one_station_linestring = "LINESTRING(31.77696 35.21658, 31.77711 35.21641)"
        result = list(query_trips_info_by_area(session=self.session,line_string_2pt=one_station_linestring))
        self.assertEqual(954, len(result),
                         'the result count size in the db don\'t match the result in the query')

    def test_query_stops_info_by_path(self):
        one_station_linestring = 'LINESTRING(35.21630 31.77732,35.21652 31.77700,35.21694 31.77644)'
        result = list(query_stops_info_by_path(session=self.session,line_string_path=one_station_linestring))
        self.assertEqual(1, len(result),
                         'the result count size in the db don\'t match the result in the query')

    def test_query_stoptimes_info_by_area(self):
        one_station_linestring = "LINESTRING(35.2083 31.7879, 35.2330 31.7747)"
        result = list(query_stoptimes_info_by_area(session=self.session, line_string_2pt=one_station_linestring))
        self.assertEqual(23813, len(result),
                         'the result count size in the db don\'t match the result in the query')

    def test_query_stoptimes_info_by_path(self):
        one_station_linestring = 'LINESTRING(35.22933 31.78803,35.23027 31.78700,35.23152 31.78503)'
        result = list(query_stoptimes_info_by_path(session=self.session, line_string_path=one_station_linestring))
        self.assertEqual(11725, len(result),
                         'the result count size in the db don\'t match the result in the query')

    def test_get_stoptimes_info_by_path(self):
        one_station_linestring = 'LINESTRING(35.22933 31.78803,35.23027 31.78700,35.23152 31.78503)'
        result = pickle.loads(get_stoptimes_info_by_path(session=self.session,line_string_path=one_station_linestring))
        self.assertEqual(11725, len(result),
                         'the result count size in the db don\'t match the result in the query')

    def test_get_stoptimes_info_by_area(self):
        one_station_linestring = "LINESTRING(35.2083 31.7879, 35.2330 31.7747)"
        result = pickle.loads(get_stoptimes_info_by_area(session=self.session, line_string_2pt=one_station_linestring))
        self.assertEqual(23813, len(result),
                         'the result count size in the db don\'t match the result in the query')

    def test_get_trips_info_by_area(self):
        one_station_linestring = "LINESTRING(35.2083 31.7879, 35.2330 31.7747)"
        result = pickle.loads(get_trips_info_by_area(session=self.session, line_string_2pt=one_station_linestring))
        self.assertEqual(0, len(result),
                         'the result count size in the db don\'t match the result in the query')
    def test_get_v_info_by_path(self):
        one_station_linestring = 'LINESTRING(35.22933 31.78803,35.23027 31.78700,35.23152 31.78503)'
        result = pickle.loads(get_v_info_by_path(session=self.session,line_string_path=one_station_linestring))

        self.assertEqual(5, len(result),
                         'the result count size in the db don\'t match the result in the query')

    @classmethod
    def tearDownClass(cls):
        drop_database(cls.engine.url)
