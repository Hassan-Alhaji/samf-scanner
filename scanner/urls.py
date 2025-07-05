from django.urls import path  # مفقودة عندك حالياً
from .views import IntakeItemViewSet, AssetViewSet, CustodyLocationViewSet, frontend_view

router = DefaultRouter()
router.register('intake', IntakeItemViewSet)
router.register('assets', AssetViewSet)
router.register('locations', CustodyLocationViewSet)

urlpatterns = router.urls + [
    path('', frontend_view),
]
