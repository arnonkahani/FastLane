from typing import List

from DB import config
from DB.gtfsdb.model.base import Base
from DB.gtfsdb.model.db import Database
from DB.gtfsdb.model.gtfs import GTFS


class GTFS_DB():
    def __init__(self):
        tables = sorted([t.name for t in Base.metadata.sorted_tables])
        self.db = self.database_load(db_url=config.DATABSE_URL, tables=tables)
        self.gtfs = self.load_data(config.GTFS_FILE_PATH)

    def database_load(self, db_url: str, tables: List[str]) -> Database:
        """This function creates Database instance for the server (only schemas i.e. no data).
        :param db_url: url of the current db.
        :type db_url: str.
        :param tables: list of the db tables.
        :type tables: list[str].
        :returns:  Database -- the database instance.
        """
        db = Database(db_url=db_url, tables=tables)
        db.create_schema(drop_all_tabels=config.SHOULD_DROP_ALL_TABELS)
        return db

    def load_data(self, file_path : str = config.GTFS_FILE_PATH) -> GTFS:
        """This function loads the db with that data from a given zip file.
        :param file_path: the path for the GTFS zip file.
        :type file_path: str.
        :returns:  GTFS -- the GTFS instance.
        """
        gtfs = GTFS(file_path)
        gtfs.load(self.db)
        return gtfs
