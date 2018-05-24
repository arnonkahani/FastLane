from DB.db.gtfs_db import GTFS_DB
from DB.db.db import Local_DB
from DB.db.passenger_count_db import PassengerCount_DB

def data_loader():
    db = Local_DB()
    db.load_schemas()
    passenger_count_db = PassengerCount_DB(db.db)
    passenger_count_db.load_data()
    gtfs = GTFS_DB(db.db)
    gtfs.load_data()

