import os
from config import Config
from mongo_connection import MongoConnection

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
CONFIG_FILE = os.path.join(BASE_DIR, 'qg-mongo-dashboard/qgmongo.conf')

CONFIG_OBJ = Config(CONFIG_FILE)
LIST_OF_NODES = CONFIG_OBJ.get_all_node_names()
ALL_NODES = CONFIG_OBJ.get_all_nodes()

MONGO_CONN = MongoConnection()

print 'constants'