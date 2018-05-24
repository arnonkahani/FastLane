from configparser import ConfigParser
from sqlalchemy_schemadisplay import create_schema_graph
import logging.config
import os
# settings.py
from dotenv import load_dotenv
# OR, explicitly providing path to '.env'
from pathlib import Path  # python3 only
env_path = os.path.dirname(os.path.realpath(__file__)) + '/.env'
load_dotenv(dotenv_path=env_path)


'''Parse configuration file and setup logging'''
config = ConfigParser()
ini_file = os.path.join(os.getcwd(), 'configs/app.ini')
config.read(ini_file)
if config.has_section('loggers'):
    logging.config.fileConfig(ini_file, disable_existing_loggers=False)


'''Application defaults'''
BATCH_SIZE = 200000
DATABSE_URL = os.getenv("DATABSE_URL")

'''Data source constants'''
DATASOURCE_GTFS = 1
DATASOURCE_LOOKUP = 2
DATASOURCE_DERIVED = 3
DATASOURCE_PASSENGERCOUNT = 4

'''Geometry constants'''
SRID = 4326

'''Order list of class names, used for creating & populating tables'''
SORTED_CLASS_NAMES = [
    'Agency',
    'Calendar',
    'Route',
    'Stop',
    'Pattern',
    'Trip',
    'StopTime',
    'RouteStop',
    'PassengerCount'
]

SHOULD_DROP_ALL_TABELS = bool(int(os.getenv("SHOULD_DROP_ALL_TABELS")))
GTFS_FILE_PATH = os.getenv("GTFS_FILE_PATH")
PASSENGER_COUNT_FILE_PATH = os.getenv("PASSENGER_COUNT_FILE_PATH")
SHOULD_LOAD_DATA = bool(int(os.getenv("SHOULD_LOAD_DATA")))
SHOULD_PASSENGER_LOAD_DATA = bool(int(os.getenv("SHOULD_PASSENGER_LOAD_DATA")))
SHOULD_OVERWRITE_ZIP_FILES = bool(int(os.getenv("SHOULD_OVERWRITE_ZIP_FILES")))
