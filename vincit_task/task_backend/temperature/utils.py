from django.db import connection
import pandas as pd
import re

DATABASE = 'iot_db.sqlite'
TABLE = 'cubesensors_data'


def sensordata_to_df():
    """
    Fetches sensordata from selected database
    returns sensordata in pandas dataframe format
    """
    sensordata_query = "SELECT * FROM {table}".format(table=TABLE)
    return pd.read_sql_query(sensordata_query, connection)


def convert_temperature(temperature):
    """
    Temperatures are saved to database as integers.
    This function converts temperatures to floats with 3 decimals.
    """
    return round(temperature/100, 3)


def escape_ansi(ansi_str):
    """
    https://www.tutorialspoint.com/How-can-I-remove-the-ANSI-escape-sequences-from-a-string-in-python
    Removes ansi coloring from string
    """
    ansi_escape = re.compile(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]')
    return ansi_escape.sub('', ansi_str)
