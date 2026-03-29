import django_filters
from django.db.models.query_utils import Q
from rest_framework.pagination import PageNumberPagination

from .models import *


# Paginacion General
class UserPagination(PageNumberPagination):
    page_size = 15
    page_size_query_param = "page_size"
    max_page_size = 1000


# Vistas de Clientes
class UserFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(label="search", method="search_data")

    class Meta:
        model = User
        fields = ["is_staff", "is_active", "profile", "activity", "search"]

    def search_data(self, queryset, name, value):
        return queryset.filter(Q(names__icontains=value) | Q(lastname__icontains=value))
