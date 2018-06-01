from contextlib import closing
import logging
import shutil
import tempfile
import time
from urllib import request
import zipfile
import os
from DB import config

log = logging.getLogger(__name__)

class_to_load_flagged = [
    ['Agency',1],
    ['Calendar',1],
    ['Route',1],
    ['Stop',1],
    ['Pattern',1],
    ['Trip',1],
    ['StopTime',1],
    ['PassengerCount',1],
    ['User',0],
    ['Analytics',0]
]


class_not_to_load_enumerated = list(filter(lambda x: not x[1], class_to_load_flagged))
class_not_to_load = list(map(lambda x: x[1],class_not_to_load_enumerated))

class GTFS(object):

    def __init__(self, filename):
        self.file = filename
        self.local_file = request.urlopen(filename)

    def load(self, db):
        '''Load GTFS into database'''
        if config.SHOULD_LOAD_DATA:
            start_time = time.time()
            log.debug('GTFS load data file: {0}'.format(self.file))
            # load known GTFS files, derived tables & lookup tables
            gtfs_directory = self.unzip(path="tmp", overwrite=config.SHOULD_OVERWRITE_ZIP_FILES)
            for cls in db.sorted_classes:
                if cls.__name__ not in class_not_to_load:
                    print("Loading {0}".format(cls.__name__))
                    cls.load(db=db, gtfs_directory=gtfs_directory)
            shutil.rmtree(gtfs_directory)
            print("Finished loading classes")
            process_time = time.time() - start_time
            log.debug('GTFS.load ({0:.0f} seconds)'.format(process_time))

    def unzip(self, path: str = None, overwrite=False):
        """This function loads the db with that data from a given zip file.
        :param path: the path for the GTFS zip file.
        :type file_path: str.
        :returns:  GTFS -- the GTFS instance.
        """
        path = path if path else tempfile.mkdtemp()
        if overwrite:
            try:
                with closing(zipfile.ZipFile(self.local_file)) as z:
                    z.extractall(path)
            except Exception as e:
                log.warning(e)
            return path
        else:
            return path
