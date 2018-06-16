import logging
import os
import time
from typing import List
from DB.db.managers.base_db import Database

log = logging.getLogger(__name__)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import object_session
import pandas as pd
from DB.db.utils.status import StatusCode


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
    def load(cls, db: Database, gtfs_directory: str) -> StatusCode:
        """This function creates Database instance for the server (only schemas i.e. no data).
        :param db: db instance.
        :type db: Databse.
        :param gtfs_directory: the GTFS temporary folder path.
        :type gtfs_directory: str.
        :returns:  StatusCode -- StatusCode.
        """
        log = logging.getLogger(cls.__module__)
        start_time = time.time()
        directory = gtfs_directory
        file_path = os.path.join(directory, cls.filename)
        if os.path.exists(file_path):
            cls.load_table_db(db, file_path)
        process_time = time.time() - start_time
        print('{0}.load ({1:.0f} seconds)'.format(cls.__name__, process_time))
        log.debug('{0}.load ({1:.0f} seconds)'.format(cls.__name__, process_time))
        return StatusCode.OK

    @classmethod
    def post_process(cls, db):
        """ Post-process processing method.  This method is a placeholder
            that may be overridden in children...
            @see: stop_time.py
        """
        pass

    @classmethod
    def get_csv_table_columns(cls) -> List[str]:
        """This function returns the table columns w/o the PK.
        :returns:  Columns -- List[str].
        """
        pass

    @classmethod
    def get_csv_table_index(cls) -> str:
        """This function returns the table PK so it can be inserted via sql to the db.
        :returns: PK -- str.
        """
        pass

    @classmethod
    def transform_data(cls, df: pd.DataFrame) -> pd.DataFrame:
        """This function transforms the dataframe so it can be inserted via sql to the db.
        :param df: url of the current db.
        :type df: Dataframe.
        :returns:  Dataframe -- the transformed dataframe.
        """
        pass

    @classmethod
    def load_table_db(cls, db: Database, file_path: str):
        """This function loads the actual data to the db table
         in case pf special loading procedure this function should be overwritten in the table class.
        :param db: the current db instance.
        :type db: Database.
        :param file_path: the current table txt file.
        :type file_path: str.
        """
        df = pd.read_csv(filepath_or_buffer=file_path)
        df = cls.transform_data(df)
        df.to_sql(con=db.engine, index_label=cls.get_csv_table_index(), name=cls.__table__.name, index=False,
                  if_exists='append')


Base = declarative_base(cls=_Base)
