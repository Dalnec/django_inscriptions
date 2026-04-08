from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404
from apps.activity.models import Activity
from .models import PageContent, MediaAsset
from .serializers import (
    PageContentSerializer,
    PageContentCreateUpdateSerializer,
    MediaAssetSerializer,
    MediaAssetUploadSerializer,
)


class PageContentViewSet(viewsets.ModelViewSet):
    queryset = PageContent.objects.all()
    serializer_class = PageContentSerializer

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return PageContentCreateUpdateSerializer
        return PageContentSerializer

    def get_queryset(self):
        queryset = PageContent.objects.all()
        activity_id = self.request.query_params.get("activity_id")
        if activity_id:
            queryset = queryset.filter(activity_id=activity_id)
        return queryset.select_related("activity")

    def create(self, request, *args, **kwargs):
        activity_id = request.data.get("activity_id") or request.data.get("activity")
        if not activity_id:
            return Response(
                {"error": "activity_id es requerido"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        activity = get_object_or_404(Activity, pk=activity_id)
        if PageContent.objects.filter(activity=activity).exists():
            return Response(
                {"error": "Ya existe contenido CMS para esta actividad"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        page_content = PageContent.objects.create(activity=activity)
        serializer = self.get_serializer(page_content, data=request.data)
        serializer.is_valid(raise_exception=True)
        for attr, value in serializer.validated_data.items():
            setattr(page_content, attr, value)
        page_content.save()
        return Response(
            PageContentSerializer(page_content, context={"request": request}).data
        )

    @action(
        detail=False,
        methods=["get", "put", "patch"],
        url_path="by-activity/(?P<activity_id>[^/.]+)",
    )
    def by_activity(self, request, activity_id=None):
        try:
            page_content = PageContent.objects.select_related("activity").get(
                activity_id=activity_id
            )
        except PageContent.DoesNotExist:
            return Response(
                {"error": "No se encontró contenido CMS para esta actividad"},
                status=status.HTTP_404_NOT_FOUND,
            )

        if request.method == "GET":
            return Response(
                PageContentSerializer(page_content, context={"request": request}).data
            )

        serializer = self.get_serializer(
            page_content, data=request.data, partial=request.method == "PATCH"
        )
        serializer.is_valid(raise_exception=True)
        for attr, value in serializer.validated_data.items():
            setattr(page_content, attr, value)
        page_content.save()
        return Response(
            PageContentSerializer(page_content, context={"request": request}).data
        )


class MediaAssetViewSet(viewsets.ModelViewSet):
    queryset = MediaAsset.objects.all()
    serializer_class = MediaAssetSerializer
    parser_classes = [MultiPartParser, FormParser]

    def get_serializer_class(self):
        if self.action == "create":
            return MediaAssetUploadSerializer
        return MediaAssetSerializer

    def get_queryset(self):
        queryset = MediaAsset.objects.all()
        activity_id = self.request.query_params.get("activity_id")
        if activity_id:
            queryset = queryset.filter(activity_id=activity_id)
        return queryset.select_related("activity")

    def perform_create(self, serializer):
        original_filename = self.request.FILES.get(
            "file", self.request.data.get("file")
        ).name
        serializer.save(original_filename=original_filename)
