from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.activity.models import Activity
from apps.activity.serializers import ActivitySerializer

from .serializers import DashboardSerializer
from .services import get_activity_dashboard


@extend_schema(tags=["Dashboard"])
class DashboardView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses={200: DashboardSerializer},
    )
    def get(self, request, activity_id):
        user = request.user
        if not (
            user.profile
            and user.profile.description
            and user.profile.description.upper() == "ADMINISTRADOR"
        ):
            return Response(
                {"detail": "No autorizado."},
                status=status.HTTP_403_FORBIDDEN,
            )

        activity = get_object_or_404(Activity, pk=activity_id)
        data = get_activity_dashboard(activity)

        serializer = DashboardSerializer(data=data)
        serializer.is_valid()
        return Response(serializer.data)
