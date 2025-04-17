from django.contrib import admin
from django.views.generic.base import RedirectView
from django.urls import path, include, reverse_lazy
from django.conf.urls.static import static
from django.conf import settings
from apps.user.views import Login, Logout
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", RedirectView.as_view(url=reverse_lazy("admin:index"))),
    # swagger
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path( "api/schema/swagger-ui/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui", ),
    path( "api/schema/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc", ),
    # Login
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/login/", Login.as_view(), name="login"),
    path("api/logout/", Logout.as_view(), name="logout"),
    # apps
    path("api/", include("apps.activity.routers"), name="activity"),
    path("api/", include("apps.user.routers"), name="user"),
    path("api/", include("apps.person.routers"), name="person"),
    path("api/", include("apps.inscription.routers"), name="inscription"),
    path("api/", include("apps.seed.routers"), name="seed"),
    path("api/", include("apps.kenani.routers"), name="kenani"),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)