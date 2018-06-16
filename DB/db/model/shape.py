import csv
import logging
from operator import itemgetter

from geoalchemy2 import Geometry
from shapely.geometry import Point
from sqlalchemy import Column, Numeric, String
from sqlalchemy.orm import relationship
from DB.db.managers.base_db import Database
from DB.config.fastlanes_config import FastlanesConfig
from DB.db.model.base import Base
import pandas as pd

__all__ = ['Pattern']

log = logging.getLogger(__name__)


class Pattern(Base):
    filename = 'shapes.txt'
    __tablename__ = 'patterns'

    shape_id = Column(String(255), primary_key=True, index=True)
    pattern_dist = Column(Numeric(20, 10))
    geom = Column(Geometry(geometry_type='LINESTRING', srid=FastlanesConfig.SRID))

    trips = relationship(
        'Trip',
        primaryjoin='Pattern.shape_id==Trip.shape_id',
        foreign_keys='(Pattern.shape_id)',
        uselist=True, viewonly=True)

    @classmethod
    def get_csv_table_columns(self):
        return self.__table__.columns.keys()

    @classmethod
    def geom_from_shape(self, points):
        return 'SRID={0};LINESTRING({1})'.format(FastlanesConfig.SRID, ','.join(points))

    @classmethod
    def get_csv_table_index(self):
        return self.__table__.columns.keys()[0]

    @classmethod
    def load_table_db(cls, db: Database, file_path: str):
        with open(file_path, mode='r', encoding="utf-8") as f:
            s = csv.reader(f)
            next(s)
            shapes = {}
            for row in s:
                if row[0] not in shapes:
                    shapes[row[0]] = []
                shapes[row[0]].append(('{0} {1}'.format(row[1], row[2]), int(row[3])))

            def geom_from_shape_helper(v):
                return cls.geom_from_shape(map(lambda x: x[0], sorted(v, key=itemgetter(1))))
            df_list = [pd.DataFrame([[k, 0, geom_from_shape_helper(v)]], columns=cls.get_csv_table_columns()) for k, v in
                 shapes.items()]
            df = pd.concat(df_list,ignore_index=True)

            df.to_sql(con=db.engine, index_label=cls.get_csv_table_index(), name=cls.__table__.name, index=False,
                      if_exists='append')
