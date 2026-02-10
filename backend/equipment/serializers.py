"""
Serializers for the equipment API.
"""
from rest_framework import serializers
from .models import UploadedDataset, DataSummary


class UploadedDatasetListSerializer(serializers.ModelSerializer):
    """Serializer for listing datasets (id, file_name, uploaded_at)."""
    class Meta:
        model = UploadedDataset
        fields = ['id', 'file_name', 'uploaded_at']


class UploadedDatasetDetailSerializer(serializers.ModelSerializer):
    """Serializer for full dataset including raw_data."""
    class Meta:
        model = UploadedDataset
        fields = ['id', 'file_name', 'uploaded_at', 'raw_data']


class DataSummarySerializer(serializers.ModelSerializer):
    """Serializer for DataSummary."""
    class Meta:
        model = DataSummary
        fields = ['id', 'total_count', 'avg_flowrate', 'avg_pressure', 'avg_temperature', 'type_distribution', 'type_stats']
