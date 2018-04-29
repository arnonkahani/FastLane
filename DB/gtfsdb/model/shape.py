import csv
import logging
from operator import itemgetter

from geoalchemy2 import Geometry
from shapely.geometry import Point
from sqlalchemy import Column, Numeric, String
from sqlalchemy.orm import relationship
from DB.gtfsdb.model.db import Database
from DB import config
from DB.gtfsdb.model.base import Base

__all__ = ['Pattern']


log = logging.getLogger(__name__)


class Pattern(Base):
    datasource = config.DATASOURCE_DERIVED
    filename = 'shapes.txt'
    __tablename__ = 'patterns'

    shape_id = Column(String(255), primary_key=True, index=True)
    pattern_dist = Column(Numeric(20, 10))
    geom = Column(Geometry(geometry_type='LINESTRING', srid=config.SRID))

    trips = relationship(
        'Trip',
        primaryjoin='Pattern.shape_id==Trip.shape_id',
        foreign_keys='(Pattern.shape_id)',
        uselist=True, viewonly=True)

    def geom_from_shape(self, points):
        #TODO : double tiple quadrple check
        coords = [Point(float(r[0]),float(r[1])) for r in points]
        coords = ['{0} {1}'.format(r.x, r.y) for r in coords]
        self.geom = 'SRID={0};LINESTRING({1})'.format(config.SRID, ','.join(coords))

    @classmethod
    def load_table_db(cls, db: Database, file_path: str):
        with open(file_path,mode='r',encoding="utf-8") as f:
            session = db.session
            s = csv.reader(f)
            next(s)
            shapes = {}
            for row in s:
                if row[0] not in shapes:
                    shapes[row[0]] = []
                shapes[row[0]].append((row[1], row[2], int(row[3])))
            for k in shapes.keys():
                shapes[k] = sorted(shapes[k], key=itemgetter(2))
            count = 0
            print(len(shapes))
            for shape_id, shape in shapes.items():
                count += 1
                pattern = cls()
                pattern.shape_id = shape_id
                if hasattr(cls, 'geom'):
                    pattern.geom_from_shape(shape)
                session.add(pattern)
                if count % 500 == 0:
                    print(count)
            session.commit()
            session.close()



