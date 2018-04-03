import pickle

from sqlalchemy.orm import Session

from DB.app import to_json
from DB.gtfsdb import Stop as queryStop, StopTime as queryStopTime , Calendar as queryCalender , Trip as queryTrip
from SharedLayer.objects.Agency import Agency
from SharedLayer.objects.Calender import Calender
from SharedLayer.objects.Path import Path
from SharedLayer.objects.PathPoint import PathPoint
from SharedLayer.objects.Route import Route
from SharedLayer.objects.Stop import Stop as Stop
from SharedLayer.objects.StopTime import StopTime
from SharedLayer.objects.Trip import Trip

def get_stoptimes_info_by_area_demo(session : Session,line_string_2pt :str):
    que = session.query(queryStop) \
        .with_entities(queryStop.stop_id,
                       queryStop.stop_name,
                       queryStop.geom,
                       queryStopTime.arrival_time,
                       queryStopTime.trip_id) \
        .filter(
        queryStop.geom.intersects(line_string_2pt)) \
        .join(queryStopTime, queryStopTime.stop_id == queryStop.stop_id)

    days = ["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"]

    def _buildStopTimeObj(record, fields):
        infoForStopTime = {}
        for index in range(len(fields)):
            infoForStopTime[fields[index]] = record[index]
        trip = Trip(infoForStopTime['trip_id'])
        stop = Stop(infoForStopTime['stop_id'], infoForStopTime['stop_name'], infoForStopTime['geom'])
        stoptime = StopTime(trip, stop, infoForStopTime['arrival_time'])
        return stoptime

    def convert_to_number(date):
        return int(date[:2]) % 24

    que2 = session.query(queryCalender).with_entities(queryCalender.service_id, queryCalender.sunday,
                                                      queryCalender.monday,
                                                      queryCalender.tuesday,
                                                      queryCalender.wednesday,
                                                      queryCalender.thursday,
                                                      queryCalender.friday,
                                                      queryCalender.saturday,
                                                      queryTrip.trip_id) \
        .join(queryTrip, queryTrip.service_id == queryCalender.service_id)


    # res_calender = [constructResponse(x, ["service_id","sunday", "monday", "tuesday", "wednesday","thursday", "friday", "saturday","trip_id"]) for x in que2]
    serives_2_dates = {}
    # for service_res in res_calender:
    #     serives_2_dates[service_res['trip_id']] = {}
    #     for day in days:
    #         serives_2_dates[service_res['trip_id']][day] = service_res[day]

    with open('gtfsdb/obj/' + "calander" + '.pkl', 'rb') as f:
        serives_2_dates = pickle.load(f)

    stopTimeArray = [_buildStopTimeObj(record , ["stop_id", "stop_name", "geom", "arrival_time", "trip_id"]) for record in que]
    pickleStopTimeArray = pickle.dumps(stopTimeArray)

    ## return pickleStopTimeArray




    data_to_send = {}
    for trip in res:
        stop_id = trip["stop_id"]
        if not stop_id in data_to_send:
            data_to_send[stop_id] = {}
            data_to_send[stop_id]['stop_id'] = trip["stop_id"]
            data_to_send[stop_id]['stop_name'] = trip["stop_name"]
            data_to_send[stop_id]['geom'] = trip["geom"]
            data_to_send[stop_id]['rides'] = []
            for i in range(7):
                data_to_send[stop_id]['rides'].append([])
                for j in range(24):
                    data_to_send[stop_id]['rides'][i].append(0)

        for idx, day in enumerate(days):
            if serives_2_dates[trip['trip_id']][day]:
                data_to_send[stop_id]['rides'][idx][convert_to_number(trip['arrival_time'])] += 1
    print(que)
    data = {"data": {"stops": list(data_to_send.values())}}
    data_json = to_json(data)
    return data_json