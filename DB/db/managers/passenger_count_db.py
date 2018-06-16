import logging
import time

from DB.db.model.passenger_count import PassengerCount

log = logging.getLogger(__name__)


class PassengerCountDB():

    def __init__(self, db, config):
        self.db = db
        self.config = config
        self.file = self.config.PASSENGER_COUNT_FILE_PATH

    def load_data(self):
        """This function loads the db with that data from a given csv file.
        """
        if self.config.SHOULD_PASSENGER_LOAD_DATA:
            start_time = time.time()
            log.debug('PassengerCount load data file: {0}'.format(self.file))
            PassengerCount.load(db=self.db, passenger_count_file=self.file)
            print("Finished loading PassengerCount")
            process_time = time.time() - start_time
            log.debug('GTFS.load ({0:.0f} seconds)'.format(process_time))
