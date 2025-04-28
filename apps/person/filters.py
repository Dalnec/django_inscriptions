import django_filters
from rest_framework.pagination import PageNumberPagination
from .models import *

class PersonFilter(django_filters.FilterSet):
    class Meta:
        model = Person
        fields = [ 'code', 'doc_num', 'names', 'lastnames', 'gender', 'birthdate', 'phone', 
                  'email', 'status', 'documenttype', 'church', 'user', ]

class PersonPagination(PageNumberPagination):
    page_size_query_param = "page_size"
    # max_page_size = 100
    page_size = 20        

    
class ChurchFilter(django_filters.FilterSet):
    class Meta:
        model = Church
        fields = [ 'description', 'active']

class ChurchPagination(PageNumberPagination):
    page_size_query_param = "page_size"
    # max_page_size = 100
    page_size = 20        


class DocumentTypeFilter(django_filters.FilterSet):
    class Meta:
        model = DocumentType
        fields = [ 'description', 'active']

class DocumentTypePagination(PageNumberPagination):
    page_size_query_param = "page_size"
    # max_page_size = 100
    page_size = 20        