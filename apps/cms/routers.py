from rest_framework.routers import DefaultRouter
from .views import PageContentViewSet, MediaAssetViewSet

router = DefaultRouter()
router.register(r"cms/pages", PageContentViewSet, basename="cms-pages")
router.register(r"cms/media", MediaAssetViewSet, basename="cms-media")

urlpatterns = router.urls
