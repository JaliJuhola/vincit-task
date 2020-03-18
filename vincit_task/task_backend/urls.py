
from django.urls import path
from django.views.generic import TemplateView
from django.urls import include, path
urlpatterns = [
    # static homepage
    path(r'', TemplateView.as_view(template_name='index.html')),
    # If more apis and versioning implemented this should be named as api/v1/temperature so additional modules can be added.
    path('api/', include('task_backend.temperature.urls')),
]
