from django.db.models.query import QuerySet
from django.shortcuts import render

from rest_framework import viewsets, mixins, generics
from .models import SH2, NCM, VIA, FComex
from .serializers import (SH2Serializer, NCMSearializer,
                            VIASearializer, FComexSearializer)

from subprocess import check_output


class SH2ViewSet(viewsets.ModelViewSet):
    
    serializer_class = SH2Serializer
    queryset = SH2.objects.all()


class NCMViewSet(viewsets.ModelViewSet):
    
    serializer_class = NCMSearializer
    queryset = NCM.objects.all()


class VIAViewSet(viewsets.ModelViewSet):
    
    serializer_class = VIASearializer
    queryset = VIA.objects.all()


class FComexViewSet(viewsets.ModelViewSet):
    
    serializer_class = FComexSearializer
    queryset = FComex.objects.all()