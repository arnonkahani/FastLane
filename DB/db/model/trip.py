import logging
log = logging.getLogger(__name__)

from sqlalchemy import Column
from sqlalchemy.orm import relationship
from sqlalchemy.types import Integer, String
from DB import config
from DB.db.model.base import Base


class Trip(Base):

    filename = 'trips.txt'

    __tablename__ = 'trips'

    route_id = Column(String(20), index=True, nullable=False)
    service_id = Column(String(20), index=True, nullable=False)
    trip_id = Column(String(20), primary_key=True, index=True, nullable=False)
    trip_headsign = Column(String(100))
    direction_id = Column(Integer, index=True)
    shape_id = Column(String(20), index=True, nullable=True)


    patterns = relationship(
        'Pattern',
        primaryjoin='Trip.shape_id==Pattern.shape_id',
        foreign_keys='(Trip.shape_id)',
        uselist=False, viewonly=True)

    route = relationship(
        'Route',
        primaryjoin='Trip.route_id==Route.route_id',
        foreign_keys='(Trip.route_id)',
        uselist=False, viewonly=True)

    stop_times = relationship(
        'StopTime',
        primaryjoin='Trip.trip_id==StopTime.trip_id',
        foreign_keys='(Trip.trip_id)',
        order_by='StopTime.stop_sequence',
        uselist=True, viewonly=True)

    calendar = relationship(
        'Calendar',
        primaryjoin='Trip.service_id==Calendar.service_id',
        foreign_keys='(Trip.service_id)',
        uselist=True, viewonly=True)

    @classmethod
    def get_csv_table_columns(self):
        return self.__table__.columns.keys()

    @classmethod
    def get_csv_table_index(self):
        return "trip_id"

    @classmethod
    def transform_data(self, df):
        if 'trip_headsign' not in df.columns:
            df['trip_headsign'] = ""
        df = df[self.get_csv_table_columns()]
        return df
