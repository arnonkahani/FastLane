import DP.logic as logic
from flask import json
import pickle
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
        Test computeNumOfBusesForStation function
        @:param : pickle object which include all the stations and the stop times for each bus
        @:return: object which include an array of all the relevant bus stations and the number of the buses per
        day and hour
        """
        result = json.loads(logic.computeNumOfBusesForStation(open_file("./mock_results/get_stoptimes_info_by_area.pkl")))
        self.assertEqual(len(result['data']['stops']), 2)

    def test_computeTripsPath(self):
        """
        Test computeNumOfBusesForStation function
        @:param : pickle object which include all the trips
        @:return: object which include an array of all the relevant bus trips
        """
        result = json.loads(logic.computeTripsPath(open_file("./mock_results/get_trips_info_by_area.pkl")))
        self.assertEqual(len(result['data']['trips']), 4025)

    def test_computeV(self):
        """
        Test computeV function
        @:param : pickle object and lat and lng for each point in the trip
        @:return: object which include an array of all the relevant bus trips
        """
        one_station_linestring = [[
            {'lat': 35.22933, 'lng': 31.78803},
            {'lat': 35.23027, 'lng': 31.78700},
            {'lat': 35.23152, 'lng': 31.78503},
        ]]
        result = json.loads(logic.computeV(open_file("./mock_results/get_v_info_by_path.pkl"), one_station_linestring))
        self.assertEqual(len(result['data']['stops']), 3)


    def test_setDefaultHours(self):
        """
        Test setDefaultHours function
        @:param : none
        @:return: two dimensional array represent a week (7 days and 24 hours for day)
        """
        result = logic.setDefaultHours()
        self.assertEqual(len(result), 24)


if __name__ == '__main__':
    unittest.main()