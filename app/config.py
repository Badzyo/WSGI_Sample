import yaml

BASE_CONFIG_PATH = 'conf/base.yml'


class Config:

    def __init__(self):
        with open(BASE_CONFIG_PATH, 'r') as base_yaml:
            self.cfg = yaml.load(base_yaml)

    @property
    def databases(self):
        return DBConfig(self.cfg)

    @property
    def server(self):
        return ServerConfig(self.cfg)


class DBConfig:
    def __init__(self, cfg):
        data = cfg['data_sourses']
        for db in data:
            setattr(self, db, data[db])


class ServerConfig:
    def __init__(self, cfg):
        data = cfg['server']
        self.host = data.get('host', 'localhost')
        self.port = data.get('port', '8000')
        self.db = data.get('db', 'postgres')

config = Config()