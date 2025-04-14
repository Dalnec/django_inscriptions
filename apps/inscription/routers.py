from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r"inscription", InscriptionView, basename="inscription")
router.register(r"paymentMethod", PaymentMethodView, basename="paymentMethod")
router.register(r"tarifa", TarifaView, basename="tarifa")
router.register(r'inscription-groups', InscriptionGroupView, basename='inscription-group')
# router.register(r"guarantor", GuarantorView, basename="guarantor")

urlpatterns = [
    path("", include(router.urls)),
]
