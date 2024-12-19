from platformdirs import *
from os import path

appname = "tim"
appauthor = "qoc"

user_data_dir = user_data_dir(appname, appauthor)
user_config_dir = user_config_dir(appname, appauthor)

EVENT_TABLE_LOCATION = path.join(user_data_dir, "event_definitions.pkl")
PROJECT_TABLE_LOCATION = path.join(user_data_dir, "project_definitions.pkl")
LOG_LOCATION = path.join(user_data_dir, "logs")
CONFIG_LOCATION = path.join(user_config_dir, "config.ini")
