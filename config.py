import os
from configparser import ConfigParser

APP = 'app'
SECRET = 'secret'

class Config:
    _instance = None

    @staticmethod
    def get_instance():
        if not Config._instance:
            Config._instance = Config()
        return Config._instance

    def __init__(self):
        self.config = ConfigParser()
        self.config.read('config.ini')

    def get_property(self, section, item):
        env_variable = "{}_{}".format(section, item)
        value = os.environ.get(env_variable)
        if not value:
            value = self.config.get(section, item)
        if value == 'None':
            return None
        return value

    @property
    def app_secret(self):
        return self.get_property(APP, SECRET)

if __name__ == '__main__':
    config = Config.get_instance()
    
    
