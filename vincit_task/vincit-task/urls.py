
from django.urls import path
from django.views.generic import TemplateView
from django.urls import include, path
urlpatterns = [
    path(r'', TemplateView.as_view(template_name='index.html'))
]
