from django.urls import path, include

#Import for routers
from rest_framework import routers

#Import for Token
# from rest_framework_simplejwt.views import (
#     TokenRefreshView,
# )

from .views import ChangePassword, Logout, UserTill, Login, PermissionView, ProfileView, UserView

router = routers.DefaultRouter()
router.register(r'users', UserView)
router.register(r'userfilter', UserTill)
router.register(r'changepassword', ChangePassword)
router.register(r'permission', PermissionView)
router.register(r'profile', ProfileView)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', Login.as_view(), name='login'),
    # path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', Logout.as_view() , name='logout'),
]
