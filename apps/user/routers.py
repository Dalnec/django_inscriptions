from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter()
router.register(r"user", UserView, basename="user")
router.register(r"profile", ProfileView, basename="user")

urlpatterns = router.urls
