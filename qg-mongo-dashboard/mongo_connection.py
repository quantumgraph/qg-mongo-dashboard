from pymongo import MongoClient

class MongoConnection(object):

    __all_connections = {}

    def get_connection(self, node_name, uri):
        if node_name not in self.__all_connections or self.__all_connections[node_name] is None:
            self.__all_connections[node_name] = MongoClient(uri)
        return self.__all_connections[node_name]