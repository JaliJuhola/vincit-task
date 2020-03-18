from django.db import connection
import pandas as pd
import requests
import re
from django.db import connection
import json

DATABASE = 'iot_db.sqlite'
TABLE = 'cubesensors_data'

def _sensordata_to_df():
    """
    Fetches sensordata from selected database
    returns sensordata in pandas dataframe format
    """
    sensordata_query = "SELECT * FROM {table}".format(table=TABLE)
    return pd.read_sql_query(sensordata_query, connection)

def _convert_temperature(temperature):
    """
    Temperatures are saved to database as integers. 
    This function converts temperatures to floats with 3 decimals.
    """
    return round(temperature/100, 3)

def _escape_ansi(ansi_str):
    """
    https://www.tutorialspoint.com/How-can-I-remove-the-ANSI-escape-sequences-from-a-string-in-python
    Removes ansi coloring from string
    """
    ansi_escape = re.compile(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]')
    return ansi_escape.sub('', ansi_str)

def aggregation_avg_and_count():
    """
    aggregates averages and counts by @sensor_id
    """
    sensordata_df = _sensordata_to_df()
    aggregations = sensordata_df.groupby('SensorId')['Temperature'].agg(['mean','count'])
    aggregations['avgTemp'] = aggregations['mean'].apply(_convert_temperature)
    aggregations = aggregations.reset_index().drop(['mean'], axis=1)
    aggregations.rename(columns={'SensorId':'sensorId'}, inplace=True)
    return json.loads(aggregations.reset_index().to_json(orient='records'))

def _get_latest_temperature_by_sensor_id(sensor_id):
    """
    Returns latests temperature of selected sensor by @sensor_id
    """
    df = _sensordata_to_df()
    df['measured'] = pd.to_datetime(df['MeasurementTime'])
    df = df.loc[df['SensorId'] == sensor_id]
    most_recent_measurement_row = df[df.MeasurementTime == df.MeasurementTime.max()]
    most_recent_measurement_value = most_recent_measurement_row['Temperature'].values[0]
    return _convert_temperature(most_recent_measurement_value)

def _get_latest_helsinki_temperature():
    """
    Returns latests temperature of sensor located in Helsinki
    """
    # wttr site seems to be pretty slow and keeps crashing constantly
    res = requests.get("http://wttr.in/Helsinki")
    current_helsinki_temperature = res.text.split(" °C")[0].split("..")[1]
    current_helsinki_temperature_without_ansi = int(_escape_ansi(current_helsinki_temperature))
    return current_helsinki_temperature_without_ansi

def aggregation_difference_to_helsinki_latest(sensor_id):
    """
    Calculates difference between current temperature in helsinki and latest temperature by @sensor_id
    """
    temperature_helsinki = _get_latest_helsinki_temperature()
    temperature_sensor = _get_latest_temperature_by_sensor_id(sensor_id)
    temperature_difference = temperature_sensor - temperature_helsinki
    return temperature_difference
