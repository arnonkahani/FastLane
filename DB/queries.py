import inspect
import pickle
from typing import Set
from flask import jsonify
from sqlalchemy.orm import Session
from DB.db import Stop, StopTime, Trip, Calendar, Pattern, Users, Analytics
from SharedLayer.objects.Path import Path as PathObj
from SharedLayer.objects.StopTime import StopTime as StopTimeObj
from SharedLayer.objects.Trip import Trip as TripObj
from SharedLayer.objects.Calender import Calender as CalenderObj
from SharedLayer.objects.Stop import Stop as StopObj
from SharedLayer.objects.Analytics import Analytics as AnalyticsObj
from SharedLayer.objects.User import User as UserObj
from geoalchemy2.shape import to_shape
from geoalchemy2 import functions
from datetime import datetime
import os
import json

demo_flag = False

    

def query_trips_info_by_area(session: Session, line_string_2pt: str):
    # Gets all stop_times and stop information in area
    return session.query(Pattern) \
        .with_entities(Pattern.shape_id,
                       Trip.trip_headsign,
                       Pattern.geom,
                       Trip.trip_id) \
        .filter(
        Pattern.geom.intersects(line_string_2pt)) \
        .join(Trip, Trip.shape_id == Pattern.shape_id)


def query_stoptimes_info_by_area(session: Session, line_string_2pt: str):
    # Gets all stop_times and stop information in area
    return session.query(Stop) \
        .with_entities(Stop.stop_id,
                       Stop.stop_name,
                       Stop.geom,
                       StopTime.arrival_time,
                       StopTime.trip_id) \
        .filter(
        Stop.geom.intersects(line_string_2pt)) \
        .join(StopTime, StopTime.stop_id == Stop.stop_id)


def query_stoptimes_info_by_path(session: Session, line_string_path: str):
    # Gets all stop_times and stop information in path
    return session.query(Stop) \
        .with_entities(Stop.stop_id,
                       Stop.stop_name,
                       Stop.geom,
                       StopTime.arrival_time) \
        .filter(
        Stop.geom.intersects(
            functions.ST_Buffer(line_string_path,
                                0.000000000000063, 'endcap=flat join=round'))) \
        .join(StopTime, StopTime.stop_id == Stop.stop_id)

def query_stops_info_by_path(session: Session, line_string_path: str):
    # Gets all stops information in path
    return session.query(Stop) \
        .with_entities(Stop.stop_id,
                       Stop.stop_name,
                       Stop.geom) \
        .filter(
        Stop.geom.intersects(
            functions.ST_Buffer(line_string_path,
                                0.000000000000063, 'endcap=flat join=round')))


def query_trips_calanders_from_set(session: Session, trips_set: Set[str]):
    # Gets all calender information of the trip from the previous query
    return session.query(Calendar).with_entities(Calendar.sunday,
                                                 Calendar.monday,
                                                 Calendar.tuesday,
                                                 Calendar.wednesday,
                                                 Calendar.thursday,
                                                 Calendar.friday,
                                                 Calendar.saturday,
                                                 Trip.trip_id) \
        .filter(Trip.trip_id.in_(trips_set)) \
        .join(Trip, Trip.service_id == Calendar.service_id)


def get_stoptimes_info_by_area(session: Session, line_string_2pt: str) -> pickle:
    """This query returns pickled stop_times information from a swuare area defined by 2 points.
    :param session: the current db session.
    :type session: Session.
    :param line_string_2pt: line string defined by 2 points.
    :type line_string_2pt: str.
    :returns:  StatusCode -- the return code.
    """
    frame = inspect.currentframe()
    function_name = inspect.getframeinfo(frame).function
    function_pkl = function_name + '.pkl'
    if not (demo_flag and os.path.isfile(function_pkl)):
        stop_stops_times_in_area = query_stoptimes_info_by_area(session, line_string_2pt)

        stop_stops_times_in_area_res = list(stop_stops_times_in_area)

        # Retrieves a set of all trip ids from the stop times
        trips_set = set(list(map(lambda x: x[4], stop_stops_times_in_area_res)))

        trip_calanders = query_trips_calanders_from_set(session, trips_set)

        trip_calanders_res = list(trip_calanders)

        # Retrieves a dictionary of all trip calenders (key: trip_id value: list of days (bool).
        trip_calanders_dict = dict((x[7], x[0:-1]) for x in trip_calanders_res)

        stops = {}
        trips = {}
        result = []

        # constructs stop_times
        for stop_time_res in stop_stops_times_in_area_res:

            stop_id = stop_time_res[0]
            stop_name = stop_time_res[1]
            stop_geom = stop_time_res[2]
            arrival_time = stop_time_res[3]
            trip_id = stop_time_res[4]

            stop_time_obj = StopTimeObj(arrival_time=arrival_time)
            if trip_id not in trips:
                trips[trip_id] = TripObj(id=trip_id, calenders=[CalenderObj(days=trip_calanders_dict[trip_id])])
            stop_time_obj.trip = trips[trip_id]

            if stop_id not in stops:
                stops[stop_id] = StopObj(id=stop_id, name=stop_name, location=to_shape(stop_geom))
            stop_time_obj.stop = stops[stop_id]

            result.append(stop_time_obj)
        with open(function_pkl, 'wb') as handle:
            pickle.dump(result, handle, protocol=pickle.HIGHEST_PROTOCOL)
    else:
        with open(function_pkl, 'rb') as handle:
            result = pickle.load(handle)

    return pickle.dumps(result)


def get_stoptimes_info_by_path(session: Session, line_string_path: str):
    """This query returns pickled stop_times information from a swuare area defined by 2 points.
    :param session: the current db session.
    :type session: Session.
    :param line_string_2pt: line string defined by 2 points.
    :type line_string_2pt: str.
    :returns:  StatusCode -- the return code.
    """
    frame = inspect.currentframe()
    function_name = inspect.getframeinfo(frame).function

    function_pkl = function_name + '.pkl'
    if not (demo_flag and os.path.isfile(function_pkl)):
        stop_stops_times_in_path = query_stoptimes_info_by_path(session, line_string_path)

        stops = {}
        result = []

        # constructs stop_times
        for stop_time_res in stop_stops_times_in_path:

            stop_id = stop_time_res[0]
            stop_name = stop_time_res[1]
            stop_geom = stop_time_res[2]
            arrival_time = stop_time_res[3]

            stop_time_obj = StopTimeObj(arrival_time=arrival_time)

            if stop_id not in stops:
                stops[stop_id] = StopObj(id=stop_id, name=stop_name, location=to_shape(stop_geom))
            stop_time_obj.stop = stops[stop_id]

            result.append(stop_time_obj)
        with open(function_pkl, 'wb') as handle:
            pickle.dump(result, handle, protocol=pickle.HIGHEST_PROTOCOL)
    else:
        with open(function_pkl, 'rb') as handle:
            result = pickle.load(handle)

    return pickle.dumps(result)


def get_trips_info_by_area(session: Session, line_string_2pt: str) -> pickle:
    """This query returns pickled trips information from a square area defined by 2 points.
    :param session: the current db session.
    :type session: Session.
    :param line_string_2pt: line string defined by 2 points.
    :type line_string_2pt: str.
    :returns:  StatusCode -- the return code.
    """
    frame = inspect.currentframe()
    function_name = inspect.getframeinfo(frame).function
    function_pkl = function_name + '.pkl'
    if not (demo_flag and os.path.isfile(function_pkl)):
        trips_in_area = query_trips_info_by_area(session, line_string_2pt)

        trips_in_area_res = list(trips_in_area)

        result = []
        # constructs trips
        for trip_res in trips_in_area_res:

            headsign = trip_res[1]
            geom = trip_res[2]
            trip_id = trip_res[3]

            trip_path = PathObj(path_line=to_shape(geom))
            trip_obj = TripObj(id=trip_id,headsign=headsign,path=trip_path)
            result.append(trip_obj)
        with open(function_pkl, 'wb') as handle:
            pickle.dump(result, handle, protocol=pickle.HIGHEST_PROTOCOL)

    else:
        with open(function_pkl, 'rb') as handle:
            result = pickle.load(handle)

    return pickle.dumps(result)

def get_v_info_by_path(session, line_string_path):
    """This query returns pickled stop_times information from a swuare area defined by 2 points.
    :param session: the current db session.
    :type session: Session.
    :param line_string_2pt: line string defined by 2 points.
    :type line_string_2pt: str.
    :returns:  StatusCode -- the return code.
    """
    frame = inspect.currentframe()
    function_name = inspect.getframeinfo(frame).function
    function_pkl = function_name +'.pkl'
    if not (demo_flag and os.path.isfile(function_pkl)):
        stops_times_in_path = query_stops_info_by_path(session, line_string_path)
        stops = {}
        result = []

        # constructs stop_times
        for stop_res in stops_times_in_path:
            stop_id = stop_res[0]
            stop_name = stop_res[1]
            stop_geom = stop_res[2]

            if stop_id not in stops:
                stops[stop_id] = StopObj(id=stop_id, name=stop_name, location=to_shape(stop_geom))

            result.append(stops[stop_id])
        with open(function_pkl, 'wb') as handle:
            pickle.dump(result, handle, protocol=pickle.HIGHEST_PROTOCOL)


    else:
        with open(function_pkl, 'rb') as handle:
            result = pickle.load(handle)



    return pickle.dumps(result)

def get_all_analytics(session):
    all_users = session.query(Users)
    users = []
    for user in all_users:
        c_user = UserObj(user.user_id)
        c_analytics = list(map(lambda analytics: AnalyticsObj(analytics.timestamp,analytics.url,analytics.event),user.events))
        c_user.analytics = c_analytics
        users.append(c_user)

    return pickle.dumps(users)

def add_user_data(session,user_data):
    user = list(session.query(Users).filter(Users.user_id == user_data["user_id"]))
    if not user:
        user = Users()
        user.user_id = user_data["user_id"]
        session.add(user)
        session.commit()

    analytics = Analytics()
    analytics.user_id = user_data["user_id"]
    analytics.event = json.dumps({"event_data":user_data["event_data"],"event_type":user_data['event_type'],"uuid":user_data["event_uuid"]})
    analytics.url = user_data["event_url"]
    analytics.timestamp = datetime.now()
    session.add(analytics)
    session.commit()
    return jsonify({})


