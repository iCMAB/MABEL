from configparser import ConfigParser
from ast import literal_eval
   
file = 'config.ini'
config = ConfigParser()
config.read(file)

config_map = config._sections

def get_config(section, key):
    return literal_eval(config_map[section][key])
