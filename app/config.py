import os
import yaml

SOURCE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_CONFIG_PATH = os.path.abspath(os.path.join(SOURCE_PATH, 'conf/base.yml'))
USER_CONFIG_PATH = os.path.abspath(os.path.join(SOURCE_PATH, 'config.yml'))


class Config:
    """
    Build configuration from basic and user yaml files
    """
    def __init__(self):
        with open(BASE_CONFIG_PATH, 'r') as base_yaml:
            base_cfg = yaml.load(base_yaml)
        with open(USER_CONFIG_PATH, 'r') as user_yaml:
            user_cfg = yaml.load(user_yaml)

        if user_cfg:
            self.cfg = self.__merge_configs(self, user_cfg, base_cfg)
        else:
            self.cfg = base_cfg

    @staticmethod
    def __merge_configs(self, user, base):
        if isinstance(user, dict) and isinstance(base, dict):
            for key, value in base.items():
                if key not in user:
                    user[key] = value
                else:
                    user[key] = self.__merge_configs(self, user[key], value)
        return user

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
        data = cfg['server'].copy()
        for key in (key for key, value in cfg['server'].items() if value is None):
            data.pop(key)
        self.host = data.get('host', 'localhost')
        self.port = data.get('port', '8080')
        self.db = data.get('db', 'postgres')

config = Config()