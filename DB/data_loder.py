from sqlalchemy.orm import sessionmaker

from DB.gtfsdb import Base
from DB.gtfsdb.gtfs_db import GTFS_DB


def data_loader():
    a = GTFS_DB()
    db = a.db
    Base.metadata.bind = db.engine
    DBSession = sessionmaker()
    session = DBSession()


if __name__ == '__main__':
    data_loader()
