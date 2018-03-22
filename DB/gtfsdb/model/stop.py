import logging
import datetime
from collections import defaultdict

from geoalchemy2 import Geometry
from sqlalchemy import Column, Integer, Numeric, String
from sqlalchemy.orm import joinedload_all, object_session, relationship

from DB.gtfsdb import config
from DB.gtfsdb.model.base import Base

log = logging.getLogger(__name__)


class Stop(Base):
    datasource = config.DATASOURCE_GTFS
    filename = 'stops.txt'

    __tablename__ = 'stops'

    stop_id = Column(String(40), primary_key=True, index=True, nullable=False)
    stop_code = Column(String(50))
    stop_name = Column(String(255), nullable=False)
    stop_desc = Column(String(255))
    stop_lat = Column(Numeric(12, 9), nullable=False)
    stop_lon = Column(Numeric(12, 9), nullable=False)
    zone_id = Column(String(50))
    location_type = Column(Integer, index=True, default=0)
    parent_station = Column(String(255))

    stop_times = relationship(
        'StopTime',
        primaryjoin='Stop.stop_id==StopTime.stop_id',
        foreign_keys='(Stop.stop_id)',
        uselist=True, viewonly=True)

    @classmethod
    def add_geometry_column(cls):
        if not hasattr(cls, 'geom'):
            cls.geom = Column(Geometry(geometry_type='POINT', srid=config.SRID))

    @classmethod
    def add_geom_to_dict(cls, row):
        args = (config.SRID, row['stop_lon'], row['stop_lat'])
        row['geom'] = 'SRID={0};POINT({1} {2})'.format(*args)
