import logging
import time
from binascii import unhexlify

from geoalchemy2 import Geometry
from sqlalchemy import Column, Integer, Numeric, String
from sqlalchemy.orm import deferred, relationship
from sqlalchemy.sql import func

from DB.gtfsdb import config
from DB.gtfsdb.model.base import Base

from shapely import wkb, wkt
from shapely.geometry import Point

__all__ = ['Pattern']


log = logging.getLogger(__name__)


class Pattern(Base):
    datasource = config.DATASOURCE_DERIVED

    __tablename__ = 'patterns'

    shape_id = Column(String(255), primary_key=True, index=True)
    pattern_dist = Column(Numeric(20, 10))

    trips = relationship(
        'Trip',
        primaryjoin='Pattern.shape_id==Trip.shape_id',
        foreign_keys='(Pattern.shape_id)',
        uselist=True, viewonly=True)

    @classmethod
    def add_geometry_column(cls):
        if not hasattr(cls, 'geom'):
            cls.geom = deferred(Column(Geometry(geometry_type='LINESTRING', srid=config.SRID)))

    # def geom_from_shape(self, points):
    #     coords = [wkb.loads(bytes(r.geom.data)) for r in points]
    #     coords = ['{0} {1}'.format(r.x, r.y) for r in coords]
    #     self.geom = 'SRID={0};LINESTRING({1})'.format(config.SRID, ','.join(coords))

    def geom_from_shape(self, points):
        #TODO : double tiple quadrple check
        coords = [Point(float(r[0]),float(r[1])) for r in points]
        coords = ['{0} {1}'.format(r.x, r.y) for r in coords]
        self.geom = 'SRID={0};LINESTRING({1})'.format(config.SRID, ','.join(coords))

    @classmethod
    def load(cls, db, **kwargs):
        start_time = time.time()
        session = db.session
        import csv
        from operator import itemgetter, attrgetter, methodcaller

        shapes = {}

        with open('{0}/shapes.txt'.format(kwargs['gtfs_directory']),
                  encoding="utf-8") as f:
            s = csv.reader(f)
            t = next(s)
            for row in s:
                if row[0] not in shapes:
                    shapes[row[0]] = []
                shapes[row[0]].append((row[1], row[2], int(row[3])))

        for k in shapes.keys():
            shapes[k] = sorted(shapes[k], key=itemgetter(2))
        count = 0
        print(len(shapes))
        for shape_id,shape in shapes.items():
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
        processing_time = time.time() - start_time
        log.debug('{0}.load ({1:.0f} seconds)'.format(
            cls.__name__, processing_time))


# class Shape(Base):
#     datasource = config.DATASOURCE_GTFS
#     filename = 'shapes.txt'
#
#     __tablename__ = 'shapes'
#
#     shape_id = Column(String(10), primary_key=True, index=True)
#     shape_pt_sequence = Column(Integer, primary_key=True, index=True)
#     shape_dist_traveled = Column(Numeric(20, 10))
#
#
#     @classmethod
#     def add_geometry_column(cls):
#         if not hasattr(cls, 'geom'):
#             cls.geom = Column(Geometry(geometry_type='POINT', srid=config.SRID))
#
#     @classmethod
#     def add_geom_to_dict(cls, row):
#         args = (config.SRID, row['shape_pt_lon'], row['shape_pt_lat'])
#         row['geom'] = 'SRID={0};POINT({1} {2})'.format(*args)
