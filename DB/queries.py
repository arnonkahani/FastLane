import pickle

from sqlalchemy.orm import Session
from DB.gtfsdb import Stop, StopTime, Trip, Calendar
from SharedLayer.objects.StopTime import StopTime as StopTimeObj
from SharedLayer.objects.Trip import Trip as TripObj
from SharedLayer.objects.Calender import Calender as CalenderObj
from SharedLayer.objects.Stop import Stop as StopObj
from geoalchemy2.shape import to_shape

def get_stoptimes_info_by_area(session: Session, line_string_2pt: str):

    stop_stops_times_in_area = session.query(Stop) \
        .with_entities(Stop.stop_id,
                       Stop.stop_name,
                       Stop.geom,
                       StopTime.arrival_time,
                       StopTime.trip_id) \
        .filter(
        Stop.geom.intersects(line_string_2pt)) \
        .join(StopTime, StopTime.stop_id == Stop.stop_id)

    stop_stops_times_in_area_res = list(stop_stops_times_in_area)
    trips_set = set(list(map(lambda x: x[4], stop_stops_times_in_area_res)))

    trip_calanders = session.query(Calendar).with_entities(Calendar.sunday,
                                             Calendar.monday,
                                             Calendar.tuesday,
                                             Calendar.wednesday,
                                             Calendar.thursday,
                                             Calendar.friday,
                                             Calendar.saturday,
                                             Trip.trip_id) \
        .filter(Trip.trip_id.in_(trips_set)) \
        .join(Trip, Trip.service_id == Calendar.service_id)

    trip_calanders_res = list(trip_calanders)
    trip_calanders_dict = dict((x[7], x[0:-1]) for x in trip_calanders_res)

    stops = {}
    trips = {}
    result = []
    for stop_time_res in stop_stops_times_in_area_res:

        stop_id = stop_time_res[0]
        stop_name = stop_time_res[1]
        stop_geom = stop_time_res[2]
        arrival_time = stop_time_res[3]
        trip_id = stop_time_res[4]

        stop_time_obj = StopTimeObj(arrival_time=arrival_time)
        if trip_id not in trips:
            trips[trip_id] = TripObj(id = trip_id,calenders= CalenderObj(days=trip_calanders_dict[trip_id]))
        stop_time_obj.trip = trips[trip_id]

        if stop_id not in stops:
            stops[stop_id] = StopObj(id=stop_id,name=stop_name,location=to_shape(stop_geom))
        stop_time_obj.stop = stops[stop_id]

        result.append(stop_time_obj)

    return pickle.dumps(result)
