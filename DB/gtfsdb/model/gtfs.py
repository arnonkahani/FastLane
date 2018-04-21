from contextlib import closing
import logging
import shutil
import tempfile
import time
from urllib import request
import zipfile

from DB.gtfsdb import config
from .route import Route

log = logging.getLogger(__name__)

class_not_to_load = [
    'Agency',
    'Calendar',
    'Route',
    'Stop',
    'Pattern',
    'Trip',
    'StopTime',
]

class_not_to_load = []


class GTFS(object):

    def __init__(self, filename):
        self.file = filename
        self.local_file = request.urlopen(filename)

    def load(self, db, shouldLoadFile=False):
        '''Load GTFS into database'''
        start_time = time.time()
        log.debug('GTFS load data file: {0}'.format(self.file))

        # load known GTFS files, derived tables & lookup tables
        gtfs_directory = self.unzip(path="tmp", overwrite=True)
        if shouldLoadFile:
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
            print("overwrite")
            try:
                with closing(zipfile.ZipFile(self.local_file)) as z:
                    z.extractall(path)
            except Exception as e:
                log.warning(e)
            return path
