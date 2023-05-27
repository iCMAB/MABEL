from configparser import ConfigParser
from ast import literal_eval
   
file = 'config.ini'
config = ConfigParser()
config.read(file)

config_map = config._sections

def get_config(section, key):
    """
    Gets the value of a key in a section of the config file.

    Args:
        section (str): The section of the config file.
        key (str): The key in the section of the config file.
    """
    return literal_eval(config_map[section][key])

def write_config(section, key, value):
    """
    Writes a value to a key in a section of the config file.

    Args:
        section (str): The section of the config file.
        key (str): The key in the section of the config file.
        value (any): The value to write to the key.
    """
    config_map[section][key] = str(value)
    with open(file, 'w') as configfile:
        config.write(configfile)