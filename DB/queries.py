import pickle

from sqlalchemy.orm import Session

from DB.app import to_json
from DB.gtfsdb import Stop, StopTime


def get_stoptimes_info_by_area_demo(session : Session,line_string_2pt :str):
    que = session.query(Stop) \
        .with_entities(Stop.stop_id,
                       Stop.stop_name,
                       Stop.geom,
                       StopTime.arrival_time,
                       StopTime.trip_id) \
        .filter(
        Stop.geom.intersects(line_string_2pt)) \
        .join(StopTime, StopTime.stop_id == Stop.stop_id)

    # que2 = session.query(Calendar).with_entities(Calendar.service_id,Calendar.sunday,
    #                    Calendar.monday,
    #                    Calendar.tuesday,
    #                    Calendar.wednesday,
    #                    Calendar.thursday,
    #                    Calendar.friday,
    #                    Calendar.saturday,
    #                    Trip.trip_id)\
    #     .join(Trip, Trip.service_id == Calendar.service_id)

    def constructResponse(row, names):
        resp = {}
        for idx in range(len(names)):
            resp[names[idx]] = row[idx]
        return resp

    def convert_to_number(date):
        return int(date[:2]) % 24

    days = ["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"]
    # res_calender = [constructResponse(x, ["service_id","sunday", "monday", "tuesday", "wednesday","thursday", "friday", "saturday","trip_id"]) for x in que2]
    serives_2_dates = {}
    # for service_res in res_calender:
    #     serives_2_dates[service_res['trip_id']] = {}
    #     for day in days:
    #         serives_2_dates[service_res['trip_id']][day] = service_res[day]

    with open('gtfsdb/obj/' + "calander" + '.pkl', 'rb') as f:
        serives_2_dates = pickle.load(f)

    res = [constructResponse(x, ["stop_id", "stop_name", "geom", "arrival_time", "trip_id"]) for x in que]
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