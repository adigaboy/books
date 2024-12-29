import configparser
import os
from pathlib import Path

config  = configparser.ConfigParser()
config.read(Path(os.getcwd(), 'etc', 'config.ini'))
