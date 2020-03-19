import json
import requests
import pandas as pd
from rest_framework.views import APIView
from rest_framework.response import Response
from task_backend.temperature.utils import convert_temperature, sensordata_to_df, escape_ansi


class TemperatureDifferenceView(APIView):
    """
    Temperature difference between get parameter sensor and current in Helsinki.
    """
    def get(self, request, sensor_id=None, format=None):
        try:
            difference_to_helsinki_latest = self.aggregation_difference_to_helsinki_latest(sensor_id)
            return Response({'difference': difference_to_helsinki_latest})
        except IndexError:
            return Response({'error': "incorrect sensorid"})

    # Aggregation methods below this could be moved to temperature/aggretations directory if initial abstraction is needed.
    def get_latest_temperature_by_sensor_id(self, sensor_id):
        """
        Returns latests temperature of selected sensor by @sensor_id
        """
        df = sensordata_to_df()
        df['measured'] = pd.to_datetime(df['MeasurementTime'])
        df = df.loc[df['SensorId'] == sensor_id]
        most_recent_measurement_row = df[df.MeasurementTime == df.MeasurementTime.max()]
        most_recent_measurement_value = most_recent_measurement_row['Temperature'].values[0]
        return convert_temperature(most_recent_measurement_value)

    def get_latest_helsinki_temperature(self):
        """
        Returns latests temperature of sensor located in Helsinki
        """
        # wttr site seems to be pretty slow and keeps crashing constantly
        res = requests.get("http://wttr.in/Helsinki")
        current_helsinki_temperature = res.text.split(" °C")[0].split("..")[1]
        current_helsinki_temperature_without_ansi = int(escape_ansi(current_helsinki_temperature))
        return current_helsinki_temperature_without_ansi

    def aggregation_difference_to_helsinki_latest(self, sensor_id):
        """
        Calculates difference between current temperature in helsinki and latest temperature by @sensor_id
        """
        temperature_helsinki = self.get_latest_helsinki_temperature()
        temperature_sensor = self.get_latest_temperature_by_sensor_id(sensor_id)
        temperature_difference = temperature_sensor - temperature_helsinki
        return temperature_difference


class SummaryView(APIView):
    """
    Returns summary of temperatures groupped by sensor
    """

    def get(self, request, format=None):
        results_by_sensor = self.aggregation_avg_and_count_by_sensor()

        return Response(data={'sensors': results_by_sensor})

    # This aggregation is pretty heavy and results so this could be scheduled and batch calculated by every minute or so.
    def aggregation_avg_and_count_by_sensor(self):
        """
        aggregates averages and counts by @sensor_id
        """
        sensordata_df = sensordata_to_df()
        aggregations = sensordata_df.groupby('SensorId')['Temperature'].agg(['mean', 'count'])
        aggregations['avgTemp'] = aggregations['mean'].apply(convert_temperature)
        aggregations = aggregations.reset_index().drop(['mean'], axis=1)
        aggregations.rename(columns={'SensorId':'sensorId'}, inplace=True)
        return json.loads(aggregations.to_json(orient='records'))
