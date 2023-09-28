import os
from configparser import ConfigParser
FILENAME = './config.ini'
_path = ''


def config(section: str = 'dbconfig'):
    global _path
    parser = ConfigParser()
    if not _path:
        _path = os.getcwd()
    parser.read(os.path.join(_path, './config.ini'))
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(f"Section {section} not found in the {FILENAME} file")
    return db

def set_config_path(path: str):
    global _path
    _path = path