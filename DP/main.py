from DP.logic import getTrips, computeNumForBusStops, computeNumOfBusesForStation
import pickle

pickelObj = pickle.load(open("data.p", "rb"))
x = computeNumOfBusesForStation(pickelObj)
print(x)