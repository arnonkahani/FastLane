import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database, database_exists, drop_database

from DB.config.fastlanes_config import FastlanesConfig
from DB.db.managers.db_manager import DBManager
from DB.db.managers.gtfs_db import GTFSDB
import DB.server as server


def create_test_db_without_schemas():
    config = FastlanesConfig(env_path=os.path.dirname(os.path.realpath(__file__)) + '/.testenv')
    config.load_config()
    engine = create_engine(config.DATABSE_URL)
    if database_exists(engine.url):
        drop_database(engine.url)
    create_database(engine.url)
    conn = engine.connect()
    conn.execute("commit")
    conn.execute("CREATE EXTENSION postgis")
    conn.close()
    return config, engine


def create_test_db_with_schemas():
    config, engine = create_test_db_without_schemas()
    config.SHOULD_DROP_ALL_TABELS = False
    db_manager = DBManager(config)
    db_manager.load_schemas()
    return config, engine, db_manager

def create_session(engine):
    # create a configured "Session" class
    Session = sessionmaker(bind=engine)

    # create a Session
    session = Session()
    return session

def create_gtfs_db():
    config, engine, db_manager = create_test_db_with_schemas()
    session = create_session(engine)
    config.SHOULD_LOAD_GTFS_DATA = True
    gtfs_db = GTFSDB(db_manager.db, config)
    gtfs_db.load_data()
    return config, engine, db_manager,session


def create_server():
    config = FastlanesConfig(env_path="./.testenv")
    server.start_server(config)
