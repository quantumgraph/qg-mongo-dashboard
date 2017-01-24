import ConfigParser

class Config(object):
    
    def __init__(self, CFILE):
        self.CFILE = CFILE
        self.cfg = ConfigParser.ConfigParser()
        a = self.cfg.read(self.CFILE)

        self.node_list = []
        for name in self.cfg.sections():
            if name[:4] == 'node':
                self.node_list.append(name[5:])

        self.node_dict = {}
        for node_name in self.node_list:
            self.node_dict[node_name] = self.get_node_config(node_name)

    def get_node_config(self, actual_node_name):
        node_name = 'node:{0}'.format(actual_node_name)
        username = self.cfg.get(node_name, 'username')
        password = self.cfg.get(node_name, 'password')
        host = self.cfg.get(node_name, 'host')
        port = self.cfg.get(node_name, 'port')
        return NodeConfig(actual_node_name, host, port, username, password)

    def get_all_node_names(self):
        return self.node_list

    def get_all_nodes(self):
        return self.node_dict


class NodeConfig(object):

    def __init__(self, node_name, host, port, username, password):
        self.node_name = node_name
        self.host = host
        self.port = port
        if not self.port:
            self.port = '27017'
        self.username = username
        self.password = password

    def get_connection_string_uri(self):
        string_uri = 'mongodb://'
        if self.username and self.password:
            string_uri += '{0}:{1}@'.format(self.host, self.port)
        string_uri += '{0}:{1}/admin'.format(self.host, self.port)
