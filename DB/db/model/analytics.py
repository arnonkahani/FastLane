from datetime import datetime

from sqlalchemy import Column, Sequence, DateTime, func, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.types import Integer, String

from DB import config
from DB.db.model.base import Base


class Analytics(Base):
    datasource = config.DATASOURCE_GTFS

    __tablename__ = 'analytics'

    id = Column(Integer, Sequence(None, optional=True), primary_key=True, nullable=True)
    timestamp = Column(DateTime, index=False,nullable=False)
    user_id = Column(String(50), index=True, nullable=False)
    url = Column(String(50), nullable=False)
    event = Column(JSON, nullable=False)


    @classmethod
    def get_csv_table_columns(self):
        return self.__table__.columns.keys()

    @classmethod
    def get_csv_table_index(self):
        return "id"

    @classmethod
    def transform_data(self, df):
        df = df[self.get_csv_table_columns()]
        return df
