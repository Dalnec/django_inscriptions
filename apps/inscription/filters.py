import django_filters
from django.db.models import F, Q
from rest_framework.pagination import PageNumberPagination
from .models import *

class InscriptionFilter(django_filters.FilterSet):
    activity = django_filters.CharFilter(field_name="group__activity__id", lookup_expr="exact")
    search = django_filters.CharFilter(method='search_filter')
    church = django_filters.CharFilter(field_name="person__church__id", lookup_expr="exact")
    
    class Meta:
        model = Inscription
        fields = [ 'checkinat', 'status', 'amount', 'observations', 'person', 
                  'activity', 'search', 'church']
    
    def search_filter(self, queryset, name, value):
        if value:
            queryset = queryset.filter(
                Q(person__doc_num__icontains=value) |
                Q(person__names__icontains=value) |
                Q(person__lastnames__icontains=value) |
                Q(group__vouchergroup__icontains=value) 
            )
        return queryset

class InscriptionPagination(PageNumberPagination):
    page_size_query_param = "page_size"
    # max_page_size = 100
    page_size = 20
        
class InscriptionGroupFilter(django_filters.FilterSet):
    class Meta:
        model = InscriptionGroup
        fields = [ "vouchergroup", "voucheramount", "activity", 
                "user", "paymentmethod", "tarifa", ]

class InscriptionPagination(PageNumberPagination):
    page_size_query_param = "page_size"
    # max_page_size = 100
    page_size = 20        

    
class PaymentMethodFilter(django_filters.FilterSet):
    class Meta:
        model = PaymentMethod
        fields = [ 'description'] 

class PaymentMethodPagination(PageNumberPagination):
    page_size_query_param = "page_size"
    # max_page_size = 100
    page_size = 20        

    
class TarifaFilter(django_filters.FilterSet):
    class Meta:
        model = Tarifa
        fields = [ 'description'] 

class TarifaPagination(PageNumberPagination):
    page_size_query_param = "page_size"
    # max_page_size = 100
    page_size = 20        