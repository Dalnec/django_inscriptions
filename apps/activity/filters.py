import django_filters
from django.db.models.query_utils import Q
from rest_framework.pagination import PageNumberPagination

from .models import *


# Paginacion General
class ActivityPagination(PageNumberPagination):
    page_size = 15
    page_size_query_param = "page_size"
    max_page_size = 1000


# Vistas de Clientes
class ActivityFilter(django_filters.FilterSet):
    # 1. Búsqueda general (Título, Descripción, Shortname)
    # Usamos 'icontains' para que no distinga entre mayúsculas y minúsculas
    search = django_filters.CharFilter(
        method="filter_search", label="Buscar en título, descripción o nombre corto"
    )

    # 2. Rango entre start_date y end_date
    # Filtra actividades que estén ocurriendo en una fecha específica
    active_in_date = django_filters.DateTimeFilter(
        method="filter_active_range", label="Actividades ocurriendo en (Fecha)"
    )

    # 3. Rango solo para fechas de inicio (start_date)
    # Permite buscar actividades que comiencen entre dos fechas
    start_date_range = django_filters.DateFromToRangeFilter(
        field_name="start_date", label="Rango de fecha de inicio (Desde/Hasta)"
    )

    class Meta:
        model = Activity
        fields = [
            "title",
            "description",
            "location",
            "start_date",
            "end_date",
            "is_active",
            # "settings",
            "shortname",
        ]

    # Lógica para la búsqueda múltiple
    def filter_search(self, queryset, name, value):
        return queryset.filter(
            models.Q(title__icontains=value)
            | models.Q(description__icontains=value)
            | models.Q(shortname__icontains=value)
        )

    # Lógica para verificar si una fecha cae dentro del evento
    def filter_active_range(self, queryset, name, value):
        return queryset.filter(start_date__lte=value, end_date__gte=value)
