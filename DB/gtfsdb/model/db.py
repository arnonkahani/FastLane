import logging

log = logging.getLogger(__file__)

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import inspect
from DB.gtfsdb import config
from DB.gtfsdb.utils.status import StatusCode


class Database(object):

    def __init__(self, tables, db_url):
        """
        keyword arguments:
            is_geospatial: if database supports geo functions
            schema: database schema name
            tables: limited list of tables to load into database
            url: SQLAlchemy database url
        """
        self.tables = tables
        self.url = db_url
        self.is_geospatial = True
        self.is_postgresql = True

    @property
    def classes(self):
        from DB.gtfsdb.model.base import Base
        if self.tables:
            return [c for c in Base.__subclasses__() if c.__tablename__ in self.tables]
        return Base.__subclasses__()

    def create_schema(self, drop_all_tabels: bool = False) -> StatusCode:
        """This function creates the table schema for FastLanes project.
        :param drop_all_tabels: a boolean argument spesfing if all tables should be dropped.
        :type drop_all_tabels: boolean.
        :returns:  StatusCode -- the return code.
        """
        ins = inspect(self.engine)
        tables = ins.get_table_names()
        try:
            for cls in self.sorted_classes:
                if drop_all_tabels:
                    cls.__table__.drop(self.engine)
                    log.debug("Dropped table schema: {0}".format(cls.__table__))
                table = str(cls.__table__)
                if not (table in tables) or drop_all_tabels:
                    cls.__table__.create(self.engine)
                    log.debug("Created table schema: {0}".format(cls.__table__))
        except:
            return StatusCode.DB_CREATE_ERROR

        return StatusCode.OK

    @property
    def dialect_name(self):
        return self.engine.url.get_dialect().name

    @property
    def metadata(self):
        from DB.gtfsdb.model.base import Base
        return Base.metadata

    @property
    def is_geospatial(self):
        return self._is_geospatial

    @is_geospatial.setter
    def is_geospatial(self, val):
        self._is_geospatial = val
        for cls in self.classes:
            if val and hasattr(cls, 'add_geometry_column'):
                cls.add_geometry_column()

    @property
    def schema(self):
        return self._schema

    @schema.setter
    def schema(self, val):
        # import pdb; pdb.set_trace()
        self._schema = val
        try:
            if self._schema:
                from sqlalchemy.schema import CreateSchema
                self.engine.execute(CreateSchema(self._schema))
        except Exception as e:
            log.info("NOTE: couldn't create schema {0} (schema might already exist)\n{1}".format(self._schema, e))

        for cls in self.classes:
            cls.__table__.schema = val

    @property
    def sorted_classes(self):
        classes = []
        for class_name in config.SORTED_CLASS_NAMES:
            cls = next((c for c in self.classes if c.__name__ == class_name), None)
            if cls:
                classes.append(cls)
        return classes

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, val):
        self._url = val
        self.engine = create_engine(val)
        session_factory = sessionmaker(self.engine)
        self.session = scoped_session(session_factory)
