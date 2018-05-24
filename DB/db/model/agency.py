from sqlalchemy import Column, Sequence
from sqlalchemy.orm import relationship
from sqlalchemy.types import Integer, String

from DB import config
from DB.db.model.base import Base


class Agency(Base):
    datasource = config.DATASOURCE_GTFS
    filename = 'agency.txt'

    __tablename__ = 'agency'

    id = Column(Integer, Sequence(None, optional=True), primary_key=True, nullable=True)
    agency_id = Column(String(40), index=True, unique=True)
    agency_name = Column(String(255), nullable=False)
    agency_url = Column(String(255), nullable=False)
    routes = relationship(
        'Route',
        primaryjoin='Route.agency_id==Agency.agency_id',
        foreign_keys='(Agency.agency_id)',
        uselist=True, viewonly=True)

    @classmethod
    def get_csv_table_columns(self):
        return self.__table__.columns.keys()[1:]

    @classmethod
    def get_csv_table_index(self):
        return "id"

    @classmethod
    def transform_data(self, df):
        df = df[self.get_csv_table_columns()]
        return df
