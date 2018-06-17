import sys
sys.path.append("./")

import DB.data_loader as data_loader
from DB.config.fastlanes_config import FastlanesConfig

from DB.server import start_server





if __name__ == '__main__':
    config = FastlanesConfig(env_path="./.env")
    config.load_config()
    data_loader.data_loader(config)
    start_server(config)