from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ConceptViewSet, MovementViewSet

router = DefaultRouter()
router.register(r"till/concepts", ConceptViewSet, basename="till-concept")
router.register(r"till/movements", MovementViewSet, basename="till-movement")

urlpatterns = [
    path("", include(router.urls)),
]

