from configparser import ConfigParser
from sqlalchemy_schemadisplay import create_schema_graph
import logging.config
import os
# settings.py
from dotenv import load_dotenv
# OR, explicitly providing path to '.env'
from pathlib import Path  # python3 only


class FastlanesConfig:

    '''Geometry constants'''
    SRID = '4326'

    '''Order list of class names, used for creating & populating tables'''
    SORTED_CLASS_NAMES =  [
        'Agency',
        'Calendar',
        'Route',
        'Stop',
        'Pattern',
        'Trip',
        'StopTime',
        'RouteStop',
        'PassengerCount',
        'Analytics',
        "Users"

    ]

    def __init__(self, env_path=None):
        # os.path.dirname(os.path.realpath(__file__)) + '/.env'
        self.env_path = env_path

    def load_config(self):
        if self.env_path:
            load_dotenv(dotenv_path=self.env_path)

        '''Parse configuration file and setup logging'''
        self.config = ConfigParser()
        ini_file = os.path.join(os.getcwd(), 'configs/app.ini')
        self.config.read(ini_file)
        if self.config.has_section('loggers'):
            logging.config.fileConfig(ini_file, disable_existing_loggers=False)

        '''Application defaults'''
        self.DATABSE_URL = os.getenv("DATABSE_URL")


        self.SHOULD_DROP_ALL_TABELS = bool(int(os.getenv("SHOULD_DROP_ALL_TABELS")))
        self.GTFS_FILE_PATH = os.getenv("GTFS_FILE_PATH")
        self.PASSENGER_COUNT_FILE_PATH = os.getenv("PASSENGER_COUNT_FILE_PATH")
        self.SHOULD_LOAD_GTFS_DATA = bool(int(os.getenv("SHOULD_LOAD_GTFS_DATA")))
        self.SHOULD_PASSENGER_LOAD_DATA = bool(int(os.getenv("SHOULD_PASSENGER_LOAD_DATA")))
        self.SHOULD_OVERWRITE_ZIP_FILES = bool(int(os.getenv("SHOULD_OVERWRITE_ZIP_FILES")))
