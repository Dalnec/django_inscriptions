import django_filters
from rest_framework.pagination import PageNumberPagination
from .models import *

class InscriptionFilter(django_filters.FilterSet):
    class Meta:
        model = Inscription
        fields = [ 'checkinat', 'status', 'amount', 'observations', 
                'person']

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