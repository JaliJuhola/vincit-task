from django.test import TestCase
import unittest.mock as mock
import pandas as pd


class TemperatureViewTestCase(TestCase):

    def setUp(self):
        self.sensor1_id = "00D5F7F8F8F8F8F8F"
        self.sensor2_id = "00A3JJ9J4Nj4Jl4K4"
        self.incorrect_sensor_id = "00A3JJ3DFNj4Jl4K4"
        testing_data = {'SensorId': [self.sensor1_id, self.sensor2_id, self.sensor1_id], 'Temperature': [2011, 2211, 805], 'MeasurementTime': ["2016-10-29 10:23:00.0000000", "2019-10-29 10:23:00.0000000", "2015-10-29 10:23:00.0000000"]}
        self.testing_dataframe = pd.DataFrame(data=testing_data)

    # TemperaturedifferenceView tests

    @mock.patch('task_backend.temperature.views.sensordata_to_df') 
    @mock.patch('task_backend.temperature.views.TemperatureDifferenceView.get_latest_helsinki_temperature')
    def test_difference_to_helsinki_latest_correct_data(self, get_latest_helsinki_temperature_mock, sensordata_to_df_mock):
        get_latest_helsinki_temperature_mock.return_value = 8
        sensordata_to_df_mock.return_value = self.testing_dataframe
        response = self.client.get('/api/diff/' + self.sensor1_id)
        self.assertEqual(response.status_code, 200)
        # Current temperature in Helsinki 8 degrees and latest of sensor 1 is 20.11
        self.assertEqual(response.json(), {'difference': 12.11})

    @mock.patch('task_backend.temperature.views.sensordata_to_df') 
    @mock.patch('task_backend.temperature.views.TemperatureDifferenceView.get_latest_helsinki_temperature')
    def test_difference_to_helsinki_latest_incorrect_sensor_id(self, get_latest_helsinki_temperature_mock, sensordata_to_df_mock):
        get_latest_helsinki_temperature_mock.return_value = 8
        sensordata_to_df_mock.return_value = self.testing_dataframe
        response = self.client.get('/api/diff/' + self.incorrect_sensor_id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'error': 'incorrect sensorid'})

    # SummaryView tests

    @mock.patch('task_backend.temperature.views.sensordata_to_df') 
    def test_summary_api(self, sensordata_to_df_mock):
        sensordata_to_df_mock.return_value = self.testing_dataframe
        response = self.client.get('/api/summary')
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(), {'sensors': [{'sensorId': '00A3JJ9J4Nj4Jl4K4', 'count': 1, 'avgTemp': 22.11}, {'sensorId': '00D5F7F8F8F8F8F8F', 'count': 2, 'avgTemp': 14.08}]})
