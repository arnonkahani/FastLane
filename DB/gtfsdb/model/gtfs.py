from contextlib import closing
import logging
import shutil
import tempfile
import time
from urllib import request
import zipfile

from gtfsdb import config
from .route import Route


log = logging.getLogger(__name__)

SORTED_CLASS_NAMES = [
    'Agency',
    'Block',
    'Calendar',
    'Route',
    'Stop',
    'Shape',
    'Pattern',
    'Trip',
    'StopTime',
]

class GTFS(object):

    def __init__(self, filename):
        self.file = filename
        self.local_file = request.urlopen(filename)

    def load(self, db, batch_size=config.BATCH_SIZE,shouldLoadFile = False):
        '''Load GTFS into database'''
        start_time = time.time()
        log.debug('GTFS.load: {0}'.format(self.file))

        # load known GTFS files, derived tables & lookup tables
        gtfs_directory = self.unzip()
        if shouldLoadFile:
            for cls in db.sorted_classes:
                if not cls.__name__ in SORTED_CLASS_NAMES:
                    print("Loading {0}".format(cls.__name__))
                    cls.load(db = db, batch_size = batch_size,gtfs_directory = gtfs_directory)
        shutil.rmtree(gtfs_directory)
        print("Finished loading classes")
        # load route geometries derived from shapes.txt
        if shouldLoadFile and False:
            if Route in db.classes:
                Route.load_geoms(db)
        if shouldLoadFile and False:
            for cls in db.sorted_classes:
                cls.post_process(db)

        process_time = time.time() - start_time
        log.debug('GTFS.load ({0:.0f} seconds)'.format(process_time))

    def unzip(self, path=None):
        """ Unzip GTFS files from URL/directory to path. """
        path = path if path else tempfile.mkdtemp()
        try:
            with closing(zipfile.ZipFile(self.local_file)) as z:
                z.extractall(path)
        except Exception as e:
            log.warning(e)
        return path
