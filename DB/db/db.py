
from typing import List

from DB import config
from DB.db.model.base import Base
from DB.db.model.db import Database
from DB.db.model.gtfs import GTFS


class Local_DB():
    def __init__(self):
        tables = sorted([t.name for t in Base.metadata.sorted_tables])
        self.db = self.database_load(db_url=config.DATABSE_URL, tables=tables)


    def database_load(self, db_url: str, tables: List[str]) -> Database:
        """This function creates Database instance for the server (only schemas i.e. no data).
        :param db_url: url of the current db.
        :type db_url: str.
        :param tables: list of the db tables.
        :type tables: list[str].
        :returns:  Database -- the database instance.
        """
        db = Database(db_url=db_url, tables=tables)
        return db

    def load_schemas(self):
        """This creates a db schemas.
        """
        self.db.create_schema(drop_all_tabels=config.SHOULD_DROP_ALL_TABELS)