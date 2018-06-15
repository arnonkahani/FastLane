import DP.logic as logic
from flask import json
import pickle
from shapely.geometry import LineString,Point
import unittest


def open_file(path):
    with (open(path, "rb")) as pickelfile:
        while True:
            try:
                contant = pickle.load(pickelfile)
                return pickle.dumps(contant)
            except EOFError:
                break


class TestLogic(unittest.TestCase):
    """
    Test the logic layer of the data processing service
    """

    def test_computeNumOfBusesForStation(self):
        """
        Test that the addition of two integers returns the correct total
        """
        result = json.loads(logic.computeNumOfBusesForStation(open_file("./mock_results/get_stoptimes_info_by_area.pkl")))
        self.assertEqual(len(result['data']['stops']), 48)

    def test_computeTripsPath(self):
       # get_trips_info_by_area.pkl
        """
        Test the addition of two strings returns the two string as one
        concatenated string
        """
        result = json.loads(logic.computeTripsPath(open_file("./mock_results/get_trips_info_by_area.pkl")))
        self.assertEqual(len(result['data']['trips']), 0)

    def test_computeV(self):
       # get_v_info_by_path.pkl
        """
        Test the addition of two strings returns the two string as one
        concatenated string
        """
        one_station_linestring = LineString([Point(0, 0), Point(1, 1)])
        result = json.loads(logic.computeV(open_file("./mock_results/get_v_info_by_path.pkl"), one_station_linestring))
        self.assertEqual(result, 'abcdef')


    def test_setDefaultHours(self):
       # get_v_info_by_path.pkl
        """
        Test the addition of two strings returns the two string as one
        concatenated string
        """
        result = logic.setDefaultHours()
        self.assertEqual(len(result), 24)


if __name__ == '__main__':
    unittest.main()