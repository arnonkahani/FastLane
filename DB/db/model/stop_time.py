import logging
import pandas as pd

from DB.db import Database
log = logging.getLogger(__name__)
import os
from sqlalchemy import Column
from sqlalchemy.orm import relationship
from sqlalchemy.types import Integer, Numeric, String

from DB.db.model.base import Base

class StopTime(Base):

    filename = 'stop_times.txt'

    __tablename__ = 'stop_times'

    trip_id = Column(String(20), primary_key=True, index=True, nullable=False)
    arrival_time = Column(String(9))
    departure_time = Column(String(9), index=True)
    stop_id = Column(String(20), index=True, nullable=False)
    stop_sequence = Column(Integer, primary_key=True, nullable=False)
    pickup_type = Column(Integer, default=0)
    drop_off_type = Column(Integer, default=0)
    shape_dist_traveled = Column(Numeric(20, 10))

    stop = relationship(
        'Stop',
        primaryjoin='Stop.stop_id==StopTime.stop_id',
        foreign_keys='(StopTime.stop_id)',
        uselist=False, viewonly=True)

    trip = relationship(
        'Trip',
        primaryjoin='Trip.trip_id==StopTime.trip_id',
        foreign_keys='(StopTime.trip_id)',
        uselist=False, viewonly=True)

    def __init__(self, *args, **kwargs):
        super(StopTime, self).__init__(*args, **kwargs)

    @classmethod
    def get_csv_table_columns(self):
        return self.__table__.columns.keys()

    @classmethod
    def get_csv_table_index(self):
        return "trip_id"

    @classmethod
    def transform_data(self, df):
        print("started preprocess")
        df = df[self.get_csv_table_columns()]
        df[["pickup_type", "drop_off_type"]] = \
            df[["pickup_type", "drop_off_type"]].fillna(0).astype(int)
        df["stop_sequence"] = \
            df["stop_sequence"].astype(int)
        df = df.drop_duplicates(["trip_id","stop_sequence"])
        print("finished preprocess")
        return df

    @classmethod
    def load_table_db(cls, db: Database, file_path: str):
        df = pd.read_csv(filepath_or_buffer=file_path)
        df = cls.transform_data(df)
        conn = db.engine.raw_connection()
        if not os.path.isdir("tmp"):
            os.mkdir("tmp")
        with open("tmp/temp_csv.csv",mode='w') as temp_file:
            df.to_csv(temp_file, index=False)
        print("Loading csv")
        with conn.cursor() as cur,open("tmp/temp_csv.csv", 'r') as f:
            columns = ','.join(cls.get_csv_table_columns())
            sql = "COPY {table_name} ({columns}) FROM STDIN WITH (FORMAT CSV, HEADER TRUE)".format(table_name=cls.__tablename__,columns=columns)
            cur.copy_expert(sql, f)
        conn.commit()


# 'trip_id,arrival_time,departure_time,stop_id,stop_sequence,pickup_type,drop_off_type,shape_dist_traveled'