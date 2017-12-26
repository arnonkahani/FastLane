from ConfigParser import ConfigParser
import logging.config
import os



'''Parse configuration file and setup logging'''
config = ConfigParser()
ini_file = os.path.join(os.getcwd(), 'configs/app.ini')
config.read(ini_file)
if config.has_section('loggers'):
    logging.config.fileConfig(ini_file, disable_existing_loggers=False)


'''Application defaults'''
BATCH_SIZE = 5000
DATABSE_URL = 'sqlite://'

'''Data source constants'''
DATASOURCE_GTFS = 1
DATASOURCE_LOOKUP = 2
DATASOURCE_DERIVED = 3

'''Geometry constants'''
SRID = 4326

'''Order list of class names, used for creating & populating tables'''
SORTED_CLASS_NAMES = [
    'RouteType',
    'RouteFilter',
    'FeedInfo',
    'Agency',
    'Block',
    'Calendar',
    'CalendarDate',
    'Route',
    'RouteDirection',
    'Stop',
    'StopFeature',
    'Transfer',
    'Shape',
    'Pattern',
    'Trip',
    'StopTime',
    'RouteStop',
    'Frequency',
    'FareAttribute',
    'FareRule',
    'UniversalCalendar',
]
