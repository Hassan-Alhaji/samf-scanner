# scanner/views.py
from django.shortcuts import render, get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import IntakeItem, Asset, CustodyLocation
from .serializers import (
    IntakeItemSerializer,
    AssetSerializer,
    CustodyLocationSerializer,
)

# =====================================================================
# ViewSets
# =====================================================================

class IntakeItemViewSet(viewsets.ModelViewSet):
    """
    واجهة CRUD لسجلات Intake (الأصول قبل الموافقة).
    لا يتطلّب تسجيل دخول من العامل.
    """
    queryset = IntakeItem.objects.all().order_by("-created_at")
    serializer_class = IntakeItemSerializer
    permission_classes: list = []  # أي شخص يستطيع الاستخدام

    @action(detail=True, methods=["post"])
    def approve(self, request, pk=None):
        """
        يعتمد السجل، يولّد رقم أصل، وينقله إلى جدول Asset.
        يُستدعى من صفحة المدير (manager.html).
        """
        item = self.get_object()

        if item.approved:
            return Response({"detail": "Already approved"}, status=400)

        asset_number = request.data.get("asset_number")
        location_id = request.data.get("location")

        if not asset_number or not location_id:
            return Response(
                {"detail": "asset_number and location required"}, status=400
            )

        if Asset.objects.filter(asset_number=asset_number).exists():
            return Response({"detail": "Asset number exists"}, status=400)

        # اعتماد السجل
        item.approved = True
        item.save()

        location = get_object_or_404(CustodyLocation, pk=location_id)
        Asset.objects.create(
            asset_number=asset_number,
            intake_item=item,
            location=location,
        )
        return Response({"detail": "Approved"}, status=status.HTTP_201_CREATED)


class AssetViewSet(viewsets.ReadOnlyModelViewSet):
    """
    عرض الأصول المعتمدة فقط (للقراءة).
    """
    queryset = Asset.objects.select_related("intake_item", "location")
    serializer_class = AssetSerializer


class CustodyLocationViewSet(viewsets.ModelViewSet):
    """
    CRUD على مواقع العهدة.
    """
    queryset = CustodyLocation.objects.all()
    serializer_class = CustodyLocationSerializer


# =====================================================================
# صفحات HTML (العامل + المدير)
# =====================================================================

def frontend_view(request):
    """
    صفحة العامل الرئيسية (index.html).
    """
    return render(request, "scanner/index.html")


def manager_view(request):
    """
    صفحة المدير لعرض الـ Intake غير المعتمدة والموافقة عليها.
    يمكنك إضافة decorator login_required إذا أردت حمايتها.
    """
    pending = IntakeItem.objects.filter(approved=False)
    locations = CustodyLocation.objects.all()
    context = {"pending": pending, "locations": locations}
    return render(request, "scanner/manager.html", context)
