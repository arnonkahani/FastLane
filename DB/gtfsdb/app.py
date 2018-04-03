from DB.gtfsdb import config
from DB.gtfsdb.model.base import Base
from DB.gtfsdb.model.db import Database
from DB.gtfsdb.model.gtfs import GTFS

class GTFS_DB():
    def __init__(self):
        tables = sorted([t.name for t in Base.metadata.sorted_tables])
        db_url = config.DATABSE_URL
        self.database_load(db_url = db_url,tabels = tables)

    def database_load(self,db_url,tabels):
        self.db = Database(db_url=db_url,tables=tabels,schema=None)
        self.db.create()
        return self.db

    def load_data(self,filename):
        self.gtfs = GTFS(filename)
        self.gtfs.load(self.db,batch_size=config.BATCH_SIZE,shouldLoadFile=False)




