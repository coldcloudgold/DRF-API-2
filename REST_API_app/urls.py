from django.urls import path
from rest_framework.routers import SimpleRouter

from .views import HandbookViewSet, ItemHandbookViewSet, ItemHandbookValidator

router = SimpleRouter()

router.register(r"handbook", HandbookViewSet, basename="handbook")
router.register(r"item_handbook", ItemHandbookViewSet, basename="item_handbook")

urlpatterns = [path("item_handbook_validator/", ItemHandbookValidator.as_view(), name="item_handbook_validator"),]

urlpatterns += router.urls
