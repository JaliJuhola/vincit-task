
from django.urls import path
from task_backend.temperature.views import SummaryView, TemperatureDifferenceView
from django.urls import include, path
urlpatterns = [
    # static homepage
    path(r'diff/<str:sensor_id>', TemperatureDifferenceView.as_view()),
    path(r'summary', SummaryView.as_view()),
]
    