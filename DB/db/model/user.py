from sqlalchemy import Column, Sequence, DateTime, func, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.types import Integer, String

from DB import config
from DB.db.model.base import Base


class Users(Base):
    datasource = config.DATASOURCE_GTFS

    __tablename__ = 'users'

    user_id = Column(String(37), primary_key=True,index=True, nullable=False)
    events = relationship(
        'Analytics',
        primaryjoin='Users.user_id==Analytics.user_id',
        foreign_keys='(Analytics.user_id)',
        uselist=False, viewonly=True)


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
