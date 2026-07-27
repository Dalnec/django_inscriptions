from django.urls import path

from .views import DashboardView

urlpatterns = [
    path(
        "activities/<int:activity_id>/dashboard/",
        DashboardView.as_view(),
        name="activity-dashboard",
    ),
]
