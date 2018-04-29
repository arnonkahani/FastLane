from sqlalchemy.orm import sessionmaker
import DB.data_loader as data_loader
from DB import config
from DB.gtfsdb import Base
from DB.gtfsdb.gtfs_db import GTFS_DB
from DB.server import app


if config.SHOULD_LOAD_DATA:
    data_loader.data_loader()


if __name__ == '__main__':
    a = GTFS_DB()
    db = a.db
    Base.metadata.bind = db.engine
    DBSession = sessionmaker()
    session = DBSession()
    app.run(debug=True, use_reloader=False, host='0.0.0.0', port=3001)