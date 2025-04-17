from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import SeedingDataViewSet
router = DefaultRouter()

router.register(r'first-data', SeedingDataViewSet, basename="Migrar Data")
urlpatterns = [
    path("", include(router.urls)),
]