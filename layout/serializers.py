from rest_framework import serializers
from .models import Box, OperationLog

class BoxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Box
        fields = '__all__'

class OperationLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = OperationLog
        fields = '__all__'
