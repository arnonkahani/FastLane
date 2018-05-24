from typing import List

from DB import config
from DB.db.model.base import Base
from DB.db.model.db import Database
from DB.db.model.gtfs import GTFS


class GTFS_DB():

    def __init__(self,db):
        self.db = db


    def load_data(self) -> GTFS:
        """This function loads the db with that data from a given zip file.
        :returns:  GTFS -- the GTFS instance.
        """
        gtfs = GTFS(config.GTFS_FILE_PATH)
        gtfs.load(self.db)
        return gtfs
