import logging

log = logging.getLogger(__name__)

from sqlalchemy import Column
from sqlalchemy.orm import relationship
from sqlalchemy.types import Integer, Numeric, String
from DB import config
from DB.gtfsdb.model.base import Base


class StopTime(Base):
    datasource = config.DATASOURCE_GTFS
    filename = 'stop_times.txt'

    __tablename__ = 'stop_times'

    trip_id = Column(String(20), primary_key=True, index=True, nullable=False)
    arrival_time = Column(String(9))
    departure_time = Column(String(9), index=True)
    stop_id = Column(String(20), index=True, nullable=False)
    stop_sequence = Column(Integer, primary_key=True, nullable=False)
    pickup_type = Column(Integer, default=0)
    drop_off_type = Column(Integer, default=0)
    shape_dist_traveled = Column(Numeric(20, 10))

    stop = relationship(
        'Stop',
        primaryjoin='Stop.stop_id==StopTime.stop_id',
        foreign_keys='(StopTime.stop_id)',
        uselist=False, viewonly=True)

    trip = relationship(
        'Trip',
        primaryjoin='Trip.trip_id==StopTime.trip_id',
        foreign_keys='(StopTime.trip_id)',
        uselist=False, viewonly=True)

    def __init__(self, *args, **kwargs):
        super(StopTime, self).__init__(*args, **kwargs)

    @classmethod
    def get_csv_table_columns(self):
        return self.__table__.columns.keys()

    @classmethod
    def get_csv_table_index(self):
        return "trip_id"

    @classmethod
    def transform_data(self, df):
        print("started preprocess")
        df = df[self.get_csv_table_columns()]
        df[["pickup_type", "drop_off_type"]] = \
            df[["pickup_type", "drop_off_type"]].fillna(0).astype(int)
        df["stop_sequence"] = \
            df["stop_sequence"].astype(int)
        df = df.drop_duplicates(["trip_id","stop_sequence"])
        print("finished preprocess")
        return df


