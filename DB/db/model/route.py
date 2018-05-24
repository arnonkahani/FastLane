import logging

log = logging.getLogger(__name__)

from sqlalchemy import Column
from sqlalchemy.orm import relationship
from sqlalchemy.types import Integer, String

from DB import config
from DB.db.model.base import Base

__all__ = ['Route']


class Route(Base):
    datasource = config.DATASOURCE_GTFS
    filename = 'routes.txt'

    __tablename__ = 'routes'

    route_id = Column(String(40), primary_key=True, index=True, nullable=False)
    agency_id = Column(String(40), index=True, nullable=True)
    route_short_name = Column(String(255))
    route_long_name = Column(String(255))
    route_desc = Column(String(1023))
    route_type = Column(Integer, index=True, nullable=False)
    route_color = Column(String(6))

    trips = relationship(
        'Trip',
        primaryjoin='Route.route_id==Trip.route_id',
        foreign_keys='(Route.route_id)',
        uselist=True, viewonly=True)

    @classmethod
    def get_csv_table_columns(self):
        return self.__table__.columns.keys()

    @classmethod
    def get_csv_table_index(self):
        return "route_id"

    @classmethod
    def transform_data(self, df):
        if 'route_desc' not in df.columns:
            df['route_desc'] = ""
        if 'route_color' not in df.columns:
            df['route_color'] = ""
        df = df[self.get_csv_table_columns()]
        return df
