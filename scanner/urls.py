# scanner/urls.py
from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import IntakeItemViewSet, AssetViewSet, CustodyLocationViewSet, frontend_view, manager_view

router = DefaultRouter()
router.register('intake', IntakeItemViewSet)
router.register('assets', AssetViewSet)
router.register('locations', CustodyLocationViewSet)

urlpatterns = router.urls + [
    path('', frontend_view),      # صفحة العامل
    path('manager/', manager_view, name='manager'),  # صفحة المدير
]