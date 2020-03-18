from rest_framework.views import APIView
from rest_framework.response import Response
from task_backend.temperature.utils import aggregation_avg_and_count, aggregation_difference_to_helsinki_latest

class TemperatureDifferenceView(APIView):
    """
    Temperature difference between get parameter sensor and current in Helsinki.
    """
    def get(self, request, sensor_id=None, format=None):
        difference_to_helsinki_latest = aggregation_difference_to_helsinki_latest(sensor_id)
        return Response({'difference': difference_to_helsinki_latest})

class SummaryView(APIView):
    """
    Returns summary of temperatures groupped by sensor
    """

    def get(self, request, format=None):
        results = aggregation_avg_and_count()
        return Response(data={'sensors': results})
