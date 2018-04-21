import logging

from sqlalchemy import Column, Sequence
from sqlalchemy.types import Integer, String

from DB import config
from DB.gtfsdb.model.base import Base

__all__ = ['Analytics']


log = logging.getLogger(__name__)


class Analytics(Base):
    datasource = config.DATASOURCE_GTFS
    __tablename__ = 'analytics'

    id = Column(Integer, Sequence(None, optional=True), primary_key=True, nullable=True)
    session_id = Column(String(37), index=True, nullable=False)
    event_type = Column(String(15),  nullable=False)
    url = Column(String(30), nullable=False)
    element_id = Column(String(30), nullable=False)


    @classmethod
    def get_csv_table_columns(self):
        return self.__table__.columns.keys()

    @classmethod
    def get_csv_table_index(self):
        return "session_id"

    @classmethod
    def transform_data(self,df):
        df = df[self.get_csv_table_columns()]
        return df


