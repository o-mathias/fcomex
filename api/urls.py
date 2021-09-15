from django.contrib import admin
from django.urls import path, include

from rest_framework import routers, urls
from app.views import SH2ViewSet, NCMViewSet, VIAViewSet, FComexViewSet

import dash_app.urls


api_router = routers.DefaultRouter()
api_router.register(r"sh2", SH2ViewSet, basename='sh2')
api_router.register(r"ncm", NCMViewSet, basename='ncm')
api_router.register(r"via", VIAViewSet, basename='via')
api_router.register(r"fcomex", FComexViewSet, basename='fcomex')

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", include(api_router.urls)),
    path('', include(dash_app.urls))
]