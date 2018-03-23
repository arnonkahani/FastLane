import logging
log = logging.getLogger(__name__)

from sqlalchemy import Column
from sqlalchemy.orm import relationship
from sqlalchemy.types import Integer, String

from DB.gtfsdb import config
from DB.gtfsdb.model.base import Base


class Trip(Base):
    datasource = config.DATASOURCE_GTFS
    filename = 'trips.txt'

    __tablename__ = 'trips'

    trip_id = Column(String(20), primary_key=True, index=True, nullable=False)
    route_id = Column(String(20), index=True, nullable=False)
    service_id = Column(String(20), index=True, nullable=False)
    direction_id = Column(Integer, index=True)
    shape_id = Column(String(20), index=True, nullable=True)
    trip_type = Column(String(20))
    trip_headsign = Column(String(100))

    # pattern = relationship(
    #     'Pattern',
    #     primaryjoin='Trip.shape_id==Pattern.shape_id',
    #     foreign_keys='(Trip.shape_id)',
    #     uselist=False, viewonly=True)

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
