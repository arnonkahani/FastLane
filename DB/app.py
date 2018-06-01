import sys
sys.path.append("./")

import DB.data_loader as data_loader
from DB import config

from DB.server import start_server





if __name__ == '__main__':
    if config.SHOULD_LOAD_DATA:
        data_loader.data_loader()
    start_server()