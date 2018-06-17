import logging

from DB.db import Database
from DB.db.utils.status import StatusCode

log = logging.getLogger(__name__)

from sqlalchemy import Column, Sequence
from sqlalchemy.orm import relationship
from sqlalchemy.types import Integer, Numeric, String
from DB import config
from DB.db.model.base import Base
import pandas as pd
import time
import os

class PassengerCount(Base):
    '''
    This is the mapping from the csv file to tabel in the DB

    IdReportRow --> passenger_count_id
    Direction --> direction
    DateKey --> date
    HourKey --> actual_time
    PlannedMissionTime --> planned_time
    StationId --> stop_id
    station_order --> stop_order
    TripId --> trip_id
    DoorsOpenTime --> door_open_time
    DoorsCloseTime --> door_close_time
    PassengersDown_rounded_sofi --> passengers_down
    PassengersUp_rounded_sofi --> passengers_up
    PassengersContinue_rounded_sofi --> passengers_continue

    '''

    filename = 'passenger_count.csv'

    __tablename__ = 'passenger_count'
    id = Column(Integer, Sequence(None, optional=True), primary_key=True, nullable=True)
    passenger_count_id = Column(String(20), index=True, nullable=False)
    direction = Column(String(1))
    date = Column(String(10))
    actual_time = Column(String(10))
    planned_time = Column(String(10))
    stop_id = Column(String(20), index=True, nullable=False)
    stop_sequence = Column(Integer, default=-1)
    trip_id = Column(String(20), index=True, nullable=False)
    door_open_time = Column(String(20))
    door_close_time = Column(String(20))
    passengers_down = Column(Integer, default=-1)
    passengers_up = Column(Integer, default=-1)
    passengers_continue = Column(Integer, default=-1)

    stop = relationship(
        'Stop',
        primaryjoin='Stop.stop_id==PassengerCount.stop_id',
        foreign_keys='(PassengerCount.stop_id)',
        uselist=False, viewonly=True)

    trip = relationship(
        'Trip',
        primaryjoin='Trip.trip_id==PassengerCount.trip_id',
        foreign_keys='(PassengerCount.trip_id)',
        uselist=False, viewonly=True)

    def __init__(self, *args, **kwargs):
        super(PassengerCount, self).__init__(*args, **kwargs)

    @classmethod
    def get_mapping(self):
        mapping = {'passenger_count_id': 'IdReportRow',
                   'direction': 'Direction',
                   'date': 'DateKey',
                   'actual_time': 'HourKey',
                   'planned_time': 'PlannedMissionTime',
                   'stop_id': 'StationId',
                   'stop_sequence': 'station_order',
                   'trip_id': 'TripId',
                   'door_open_time': 'DoorsOpenTime',
                   'door_close_time': 'DoorsCloseTime',
                   'passengers_down': 'PassengersDown_rounded_sofi',
                   'passengers_up': 'PassengersUp_rounded_sofi',
                   'passengers_continue': 'PassengersContinue_rounded_sofi'}
        return mapping

    @classmethod
    def get_csv_table_columns(self):
        return self.__table__.columns.keys()

    @classmethod
    def get_csv_table_index(self):
        return "id"

    @classmethod
    def get_mapping_to_csv(self, column):
        mapping = self.get_mapping()
        return mapping[column]

    @classmethod
    def transform_data(self, df):
        print("started preprocess")
        df = df[list(self.get_mapping().values())]
        new_df = pd.DataFrame(columns=self.__table__.columns.keys())
        for column in list(self.__table__.columns.keys())[1:-1]:
            new_df[column] = df[self.get_mapping_to_csv(column)]
        new_df[self.get_csv_table_index()] = list(range(new_df[list(self.__table__.columns.keys())[2]].count()))
        print("finished preprocess")
        return new_df

    @classmethod
    def load(cls, db: Database, passenger_count_file: str) -> StatusCode:
        """This function creates Database instance for the server (only schemas i.e. no data).
        :param db: db instance.
        :type db: Databse.
        :param gtfs_directory: the GTFS temporary folder path.
        :type gtfs_directory: str.
        :returns:  StatusCode -- StatusCode.
        """
        log = logging.getLogger(cls.__module__)
        start_time = time.time()
        if os.path.exists(passenger_count_file):
            cls.load_table_db(db, passenger_count_file)
        process_time = time.time() - start_time
        print('{0}.load ({1:.0f} seconds)'.format(cls.__name__, process_time))
        log.debug('{0}.load ({1:.0f} seconds)'.format(cls.__name__, process_time))
        return StatusCode.OK
