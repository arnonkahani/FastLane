from DB.db.managers.gtfs_db import GTFSDB
from DB.db.managers .db_manager import DBManager
from DB.db.managers.passenger_count_db import PassengerCountDB

def data_loader(config):
    db = DBManager(config=config)
    db.load_schemas()
    passenger_count_db = PassengerCountDB(db.db,config=config)
    passenger_count_db.load_data()
    gtfs = GTFSDB(db.db,config=config)
    gtfs.load_data()

