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



