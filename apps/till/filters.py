import django_filters
from django.db.models import Q
from rest_framework.pagination import PageNumberPagination

from .models import Concept, Movement


class ConceptFilter(django_filters.FilterSet):
    class Meta:
        model = Concept
        fields = ["description", "concept_type", "is_active", "is_internal"]


class ConceptPagination(PageNumberPagination):
    page_size_query_param = "page_size"
    page_size = 20


class MovementFilter(django_filters.FilterSet):
    activity = django_filters.NumberFilter(field_name="activity_id")
    concept = django_filters.NumberFilter(field_name="concept_id")
    concept_type = django_filters.CharFilter(field_name="concept__concept_type")
    movement_at_from = django_filters.DateTimeFilter(
        field_name="movement_at", lookup_expr="gte"
    )
    movement_at_to = django_filters.DateTimeFilter(
        field_name="movement_at", lookup_expr="lte"
    )
    search = django_filters.CharFilter(method="search_filter")
    activity_shortname = django_filters.CharFilter(
        field_name="activity__shortname", lookup_expr="exact"
    )

    class Meta:
        model = Movement
        fields = [
            "status",
            "activity",
            "activity_shortname",
            "concept",
            "concept_type",
            "inscription",
            "inscription_group",
            "user",
            "payment_method",
            "movement_at_from",
            "movement_at_to",
            "search",
        ]

    def search_filter(self, queryset, name, value):
        if value:
            queryset = queryset.filter(
                Q(description__icontains=value) | Q(reference__icontains=value)
            )
        return queryset


class MovementPagination(PageNumberPagination):
    page_size_query_param = "page_size"
    page_size = 20
