import os
from configparser import ConfigParser

APP = 'app'
SID = 'sid'
TWILIO_TOKEN='twilio_token'
ACTIVE_NUMBER = 'active_number'

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
    def app_sid(self):
        return self.get_property(APP, SID)
    @property
    def app_twilio(self):
        return self.get_property(APP, TWILIO_TOKEN)
    @property
    def app_active_number(self):
        return self.get_property(APP, ACTIVE_NUMBER )

if __name__ == '__main__':
    config = Config.get_instance()
    
    
