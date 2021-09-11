from rest_framework import serializers
from .models import SH2, NCM, VIA, FComex


class SH2Serializer(serializers.ModelSerializer):

    class Meta:
        model = SH2
        fields = '__all__'


class NCMSearializer(serializers.ModelSerializer):

    class Meta:
        model = NCM
        fields = '__all__'


class VIASearializer(serializers.ModelSerializer):

    class Meta:
        model = VIA
        fields = '__all__'


class FComexSearializer(serializers.ModelSerializer):

    class Meta:
        model = FComex
        fields = '__all__'