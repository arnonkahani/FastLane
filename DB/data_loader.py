from DB.gtfsdb.gtfs_db import GTFS_DB


def data_loader():
    a = GTFS_DB()
    a.load_schemas()
    a.load_data()

