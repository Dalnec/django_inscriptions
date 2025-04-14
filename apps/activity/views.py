from rest_framework import generics, viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema
from django_filters.rest_framework import DjangoFilterBackend

from .models import *
from .serializers import *
from .filters import *

@extend_schema(tags=["Activity"])
class ActivityView(viewsets.ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer