from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r"person", PersonView, basename="person")
router.register(r"church", ChurchView, basename="church")
router.register(r"documentType", DocumentTypeView, basename="documentType")
router.register(r"kind", KindView, basename="kind")
# router.register(r"guarantor", GuarantorView, basename="guarantor")

urlpatterns = [
    path("", include(router.urls)),
]
