import logging

from geoalchemy2 import Geometry
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from DB.config.fastlanes_config import FastlanesConfig
from DB.db.model.base import Base

log = logging.getLogger(__name__)


class Stop(Base):

    filename = 'stops.txt'

    __tablename__ = 'stops'

    stop_id = Column(String(40), primary_key=True, index=True, nullable=False)
    stop_code = Column(String(50))
    stop_name = Column(String(255), nullable=False)
    stop_desc = Column(String(255))
    zone_id = Column(String(50))
    location_type = Column(Integer, index=True, default=0)
    parent_station = Column(String(255))
    geom = Column(Geometry(geometry_type='POINT', srid=FastlanesConfig.SRID))

    stop_times = relationship(
        'StopTime',
        primaryjoin='Stop.stop_id==StopTime.stop_id',
        foreign_keys='(Stop.stop_id)',
        uselist=True, viewonly=True)

    @classmethod
    def get_csv_table_columns(self):
        return self.__table__.columns.keys()

    @classmethod
    def get_csv_table_index(self):
        return "stop_id"

    @classmethod
    def transform_data(self, df):
        df['geom'] = df.apply(lambda x: 'SRID={0};POINT({1} {2})'.format(FastlanesConfig.SRID, x.stop_lat, x.stop_lon), axis=1)

        if 'zone_id' not in df.columns:
            df['zone_id'] = ""
        if 'location_type' not in df.columns:
            df['location_type'] = 1
        if 'parent_station' not in df.columns:
            df['parent_station'] = ""

        df = df[self.get_csv_table_columns()]
        return df
