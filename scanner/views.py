from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status, viewsets
from .models import IntakeItem, Asset, CustodyLocation
from .serializers import IntakeItemSerializer, AssetSerializer, CustodyLocationSerializer

class IntakeItemViewSet(viewsets.ModelViewSet):
    queryset = IntakeItem.objects.all().order_by('-created_at')
    serializer_class = IntakeItemSerializer

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        item = self.get_object()
        if item.approved:
            return Response({'detail': 'Already approved'}, status=400)
        asset_number = request.data.get('asset_number')
        location_id  = request.data.get('location')
        if not asset_number or not location_id:
            return Response({'detail': 'asset_number and location required'}, status=400)
        # تأكيد عدم التكرار
        if Asset.objects.filter(asset_number=asset_number).exists():
            return Response({'detail': 'Asset number exists'}, status=400)
        item.approved = True
        item.save()
        location = CustodyLocation.objects.get(pk=location_id)
        Asset.objects.create(asset_number=asset_number, intake_item=item, location=location)
        return Response({'detail': 'Approved'}, status=status.HTTP_201_CREATED)

class AssetViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Asset.objects.select_related('intake_item', 'location')
    serializer_class = AssetSerializer

class CustodyLocationViewSet(viewsets.ModelViewSet):
    queryset = CustodyLocation.objects.all()
    serializer_class = CustodyLocationSerializer