import pickle
import unittest

from sqlalchemy_utils import drop_database

from DB.queries import query_trips_info_by_area, query_stops_info_by_path, query_stoptimes_info_by_area, \
    query_stoptimes_info_by_path, get_trips_info_by_area, get_stoptimes_info_by_path, get_v_info_by_path, \
    get_stoptimes_info_by_area
from DB.tests.test_utils import create_gtfs_db

area_query_linestring = 'LINESTRING(31.78767 35.22943,31.78690 35.23077)'
path_query_linestring = 'LINESTRING(31.78762 35.22973,31.78655 35.23072,31.78638 35.23077,31.78603 35.22991)'
v_path_query_linestring = 'LINESTRING(31.78803 35.22933,31.78700 35.23027,31.78503 35.23152)'


class GTFSLoadTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.config, cls.engine, cls.db_manager, cls.session = create_gtfs_db()

    def test_get_stoptimes_info_by_path(self):
        result = pickle.loads(get_stoptimes_info_by_path(session=self.session, line_string_path=path_query_linestring))
        self.assertEqual(6848, len(result),
                         'the result count size in the db don\'t match the result in the query')

    def test_get_stoptimes_info_by_area(self):
        result = pickle.loads(get_stoptimes_info_by_area(session=self.session, line_string_2pt=area_query_linestring))
        self.assertEqual(2180, len(result),
                         'the result count size in the db don\'t match the result in the query')

    def test_get_trips_info_by_area(self):
        result = pickle.loads(get_trips_info_by_area(session=self.session, line_string_2pt=area_query_linestring))
        self.assertEqual(4025, len(result),
                         'the result count size in the db don\'t match the result in the query')

    def test_get_v_info_by_path(self):
        result = pickle.loads(get_v_info_by_path(session=self.session, line_string_path=v_path_query_linestring))
        self.assertEqual(5, len(result),
                         'the result count size in the db don\'t match the result in the query')

    @classmethod
    def tearDownClass(cls):
        drop_database(cls.engine.url)
