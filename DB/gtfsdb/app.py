from gtfsdb import config
from gtfsdb.model.base import Base
from gtfsdb.model.db import Database
from gtfsdb.model.gtfs import GTFS

class GTFS_DB():
    def __init__(self):
        tables = sorted([t.name for t in Base.metadata.sorted_tables])
        batch_size = config.BATCH_SIZE
        db_url = config.DATABSE_URL
        self.database_load(db_url = db_url,batch_size = batch_size,tabels = tables)

    def database_load(self,db_url,batch_size,tabels):
        db = Database(db_url,batch_size,tabels)
        db.create()
        return db

    def load_data(self,filename):
        gtfs = GTFS(filename)
        gtfs.load(db,batch_size=config.BATCH_SIZE)




