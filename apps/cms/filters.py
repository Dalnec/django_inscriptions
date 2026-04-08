from django_filters import rest_framework as filters
from .models import PageContent, MediaAsset


class PageContentFilter(filters.FilterSet):
    activity_id = filters.NumberFilter(field_name="activity__id")
    theme_color = filters.CharFilter(field_name="theme_color")

    class Meta:
        model = PageContent
        fields = ["activity_id", "theme_color"]


class MediaAssetFilter(filters.FilterSet):
    activity_id = filters.NumberFilter(field_name="activity__id")

    class Meta:
        model = MediaAsset
        fields = ["activity_id"]
