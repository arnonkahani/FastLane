from typing import List

from DB import config
from DB.db.model.base import Base
from DB.db.model.db import Database
from DB.db.model.passenger_count_loader import PassengerCountLoader


class PassengerCount_DB():

    def __init__(self,db):
        self.db = db


    def load_data(self) -> PassengerCountLoader:
        """This function loads the db with that data from a given csv file.
        :returns:  PassengerCountLoader -- the PassengerCountLoader instance.
        """
        passenger_loader = PassengerCountLoader(config.PASSENGER_COUNT_FILE_PATH)
        passenger_loader.load(self.db)
        return passenger_loader
