import logging

from DB.gtfsdb import config
from DB.gtfsdb.model.base import Base
from sqlalchemy import Column, Index
from sqlalchemy.types import Boolean, Date, String
import pandas as pd

__all__ = ['Calendar']


log = logging.getLogger(__name__)


class Calendar(Base):
    datasource = config.DATASOURCE_GTFS
    filename = 'calendar.txt'

    __tablename__ = 'calendar'
    __table_args__ = (Index('calendar_ix1', 'start_date', 'end_date'),)

    service_id = Column(String(30), primary_key=True, index=True, nullable=False)
    monday = Column(Boolean, nullable=False)
    tuesday = Column(Boolean, nullable=False)
    wednesday = Column(Boolean, nullable=False)
    thursday = Column(Boolean, nullable=False)
    friday = Column(Boolean, nullable=False)
    saturday = Column(Boolean, nullable=False)
    sunday = Column(Boolean, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)

    def weekday_list(self):
        return [self.sunday,self.monday,self.tuesday,self.wednesday,self.thursday,self.friday,self.saturday]

    @classmethod
    def get_csv_table_columns(self):
        return self.__table__.columns.keys()

    @classmethod
    def get_csv_table_index(self):
        return "service_id"

    @classmethod
    def transform_data(self,df):
        df = df[self.get_csv_table_columns()]
        df[["sunday","monday","tuesday","wednesday","thursday","friday","saturday"]] =\
            df[["sunday","monday","tuesday","wednesday","thursday","friday","saturday"]].astype(bool)
        df["start_date"] = pd.to_datetime(df["start_date"],yearfirst=True,format='%Y%m%d')
        df["end_date"] = pd.to_datetime(df["end_date"],yearfirst=True,format='%Y%m%d')
        return df


