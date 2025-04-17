from django.urls import include, path
from rest_framework.routers import DefaultRouter

# from .views import ExtractingDataViewSet

router = DefaultRouter()
# router.register(r'get_data', ExtractingDataViewSet, basename="Extracting Data")
urlpatterns = [
    path("", include(router.urls)),
]