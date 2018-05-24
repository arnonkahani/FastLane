from contextlib import closing
import logging
import shutil
import tempfile
import time
from urllib import request
import zipfile
import os
from DB import config
from DB.db.model.passenger_count import PassengerCount

log = logging.getLogger(__name__)


class PassengerCountLoader(object):

    def __init__(self, filename):
        self.file = filename

    def load(self, db):
        '''Load PassengerCount into database'''
        if config.SHOULD_PASSENGER_LOAD_DATA:
            start_time = time.time()
            log.debug('PassengerCount load data file: {0}'.format(self.file))
            PassengerCount.load(db=db, passenger_count_file=self.file)
            print("Finished loading PassengerCount")
            process_time = time.time() - start_time
            log.debug('GTFS.load ({0:.0f} seconds)'.format(process_time))

