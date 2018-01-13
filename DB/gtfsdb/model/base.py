import csv
from datetime import datetime
import os
import time
import logging
log = logging.getLogger(__name__)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import object_session
from geoalchemy2.shape import to_shape
from shapely.geometry import mapping
from geoalchemy2.elements import WKBElement
import json
from sqlalchemy.ext.declarative import DeclarativeMeta

class _Base(object):

    filename = None

    @property
    def session(self):
        ret_val = None
        try:
            ret_val = object_session(self)
        except:
            log.warn("can't get a session from object")
        return ret_val

    @classmethod
    def make_geom_lazy(cls):
        from sqlalchemy.orm import deferred 
        try:
            cls.__mapper__.add_property('geom', deferred(cls.__table__.c.geom))
        except Exception as e:
            log.warn(e)

    @classmethod
    def from_dict(cls, attrs):
        clean_dict = cls.make_record(attrs)
        return cls(**clean_dict)


    def to_dict(self, rel=None, backref=None):
        if rel is None:
            rel = False
        res = {column.key: getattr(self, attr)
               for attr, column in self.__mapper__.c.items()}
        if rel:
            for attr, relation in self.__mapper__.relationships.items():
                # Avoid recursive loop between to tables.
                if backref == relation.table:
                    continue
                value = getattr(self, attr)
                if value is None:
                    res[relation.key] = None
                elif isinstance(value.__class__, DeclarativeMeta):
                    res[relation.key] = value.to_dict(backref=self.__table__)
                else:
                    res[relation.key] = [i.to_dict(backref=self.__table__)
                                         for i in value]
        return res

    def __iter__(self):
        return self.to_dict().iteritems()

    @property
    def to_json(self, rel=None):
        def extended_encoder(x):
            if isinstance(x, WKBElement):
                return mapping(to_shape(x))
            if isinstance(x, datetime):
                return x.isoformat()
        if rel is None:
            rel = False
        dict_t = self.to_dict(rel)
        return json.dumps(dict_t, default=extended_encoder)

    def get_up_date_name(self, attribute_name):
        """ return attribute name of where we'll store an update variable
        """
        return "{0}_update_utc".format(attribute_name)

    def is_cached_data_valid(self, attribute_name, max_age=2):
        """ we have to see both the attribute name exist in our object, as well as
            that object having a last update date (@see update_cached_data below)
            and that update date being less than 2 days ago...
        """
        ret_val = False
        try:
            #import pdb; pdb.set_trace()
            if hasattr(self, attribute_name):
                attribute_update = self.get_up_date_name(attribute_name)
                if hasattr(self, attribute_update):
                    epoch = datetime.datetime.utcfromtimestamp(0)
                    delta = getattr(self, attribute_update) - epoch
                    if delta.days <= max_age:
                        ret_val = True
        except:
            log.warn("is_cached_data_valid(): saw a cache exception with attribute {0}".format(attribute_name))
            ret_val = False

        return ret_val

    def update_cached_data(self, attribute_name):
        """
        """
        try:
            #import pdb; pdb.set_trace()
            attribute_update = self.get_up_date_name(attribute_name)
            setattr(self, attribute_update, datetime.datetime.now())
        except:
            log.warn("update_cached_data(): threw an exception with attribute {0}".format(attribute_name))

    @classmethod
    def load(cls, db, batch_size,gtfs_directory):
        """Load method for ORM

        arguments:
            db: instance of gtfsdb_1.Database

        keyword arguments:
            gtfs_directory: path to unzipped GTFS files
            batch_size: batch size for memory management
        """
        log = logging.getLogger(cls.__module__)
        start_time = time.time()
        directory = gtfs_directory
        records = []
        file_path = os.path.join(directory, cls.filename)
        if os.path.exists(file_path):
            f = open(file_path, 'r',encoding="utf-8")
            reader = csv.DictReader(f)
            reader.fieldnames = [field.strip().lower() for field in reader.fieldnames]
            table = cls.__table__
            try:
                db.engine.execute(table.delete())
            except:
                log.debug("NOTE: couldn't delete this table")

            i = 0
            for row in reader:
                records.append(cls.make_record(row))
                i += 1
                if i >= batch_size:
                    db.engine.execute(table.insert(), records)
                    print('*')
                    records = []
                    i = 0
            if len(records) > 0:
                db.engine.execute(table.insert(), records)
            f.close()
        process_time = time.time() - start_time
        print('{0}.load ({1:.0f} seconds)'.format(cls.__name__, process_time))
        log.debug('{0}.load ({1:.0f} seconds)'.format(cls.__name__, process_time))

    @classmethod
    def post_process(cls, db):
        """ Post-process processing method.  This method is a placeholder
            that may be overridden in children...
            @see: stop_time.py
        """
        pass

    @classmethod
    def make_record(cls, row):
        for k, v in list(row.items()):
            if isinstance(v, (str,bytes)):
                row[k] = v.strip()

            try:
                if k:
                    # if (k not in cls.__table__.c):
                    #     del row[k]
                    if not v:
                        row[k] = None
                    elif k.endswith('date'):
                        row[k] = datetime.datetime.strptime(v, '%Y%m%d').date()
                else:
                    log.info("I've got issues with your GTFS {0} data.  I'll continue, but expect more errors...".format(cls.__name__))
            except Exception as e:
                log.warning(e)

        """if this is a geospatially enabled database, add a geom"""
        if hasattr(cls, 'geom') and hasattr(cls, 'add_geom_to_dict'):
            cls.add_geom_to_dict(row)
        return row


Base = declarative_base(cls=_Base)
