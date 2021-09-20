from django.contrib import admin
from django.urls import include, path
from django.conf.urls import url

from django.views.generic import TemplateView

from django.conf import settings
from django.conf.urls.static import static

from django_plotly_dash.views import add_to_session

from .views import dash_view

urlpatterns = [
    path('dash', dash_view, name="dash"),
    path('django_plotly_dash/', include('django_plotly_dash.urls')),
]
