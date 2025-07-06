# scanner/serializers.py
from rest_framework import serializers
from .models import IntakeItem, Asset, CustodyLocation

class IntakeItemSerializer(serializers.ModelSerializer):
    uploader = serializers.StringRelatedField(read_only=True)
    class Meta:
        model  = IntakeItem
        fields = '__all__'
        read_only_fields = ('approved', 'uploader')

class AssetSerializer(serializers.ModelSerializer):
    intake_item = IntakeItemSerializer(read_only=True)

    class Meta:
        model = Asset
        fields = '__all__'

class CustodyLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustodyLocation
        fields = '__all__'