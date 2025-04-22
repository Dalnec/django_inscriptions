import requests
from rest_framework import generics, viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema
from django_filters.rest_framework import DjangoFilterBackend
from .models import *
from .serializers import *
from .filters import *

# Create your views here.
@extend_schema(tags=["Person"])
class PersonView(viewsets.GenericViewSet):
    serializer_class = PersonSerializer
    queryset = Person.objects.all().order_by("id")
    filter_backends = [DjangoFilterBackend]
    filterset_class = PersonFilter
    pagination_class = PersonPagination

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def destroy(self, request, pk=None):
        instance = self.get_object()
        if request.user.is_owner:
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        
        return Response(
            {"message": "No tiene permisos para realizar esta accion"},
            status=status.HTTP_403_FORBIDDEN,
        )
    
    @action(detail=False, methods=["get"], url_path="apiclient/(?P<document>[0-9]+)")
    def apiclient(self, request, document=None):
        [token, url] = ["98b6cb649290e8ffff6f3041b6f57d2d7e26ee816182052ff88444dd2505b0ce", "https://my.apidev.pro/api"]
        header = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {}'.format(token)
        }
        
        if len(document) == 8:
            url = f'{url}/dni/' + document
        elif len(document) == 11:
            url = f'{url}/ruc/' + document
        else:
            return  Response({"success": False, "message":f"{document} No es un documento válido"})
        
        person = Person.objects.filter(doc_num=document)
        if person.exists():
            person = person.first()
            return Response({
                "success": True, 
                "message":f"{document} ya existe", 
                "data": {
                    "created":person.created.strftime("%Y-%m-%d %H:%M:%S"),
                    "code":person.code,
                    "doc_num":person.doc_num,
                    "names":person.names,
                    "lastnames":person.lastnames,
                    "gender":person.gender,
                    "birthday":person.birthday,
                    "phone":person.phone,
                    "email":person.email,
                    "status":person.status,
                    "kind":person.kind,
                    "documenttype":person.documenttype.id,
                    "church":person.church,
                    "user":person.user,
                }
            })
            
        response = requests.get(url, headers=header, verify=False)
        if response.status_code == 200:
            return  Response(response.json())
        elif response.status_code == 404:
            return  Response({"success": False, "message":"Not Found!"})
        else:
            return  Response({"success": False, "message":"Error!"})

@extend_schema(tags=["Church"])
class ChurchView(viewsets.GenericViewSet):
    serializer_class = ChurchSerializer
    queryset = Church.objects.all().order_by("id")
    filter_backends = [DjangoFilterBackend]
    filterset_class = ChurchFilter
    pagination_class = ChurchPagination

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def destroy(self, request, pk=None):
        instance = self.get_object()
        if request.user.is_owner:
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        
        return Response(
            {"message": "No tiene permisos para realizar esta accion"},
            status=status.HTTP_403_FORBIDDEN,
        )

@extend_schema(tags=["DocumentType"])
class DocumentTypeView(viewsets.GenericViewSet):
    serializer_class = DocumentTypeSerializer
    queryset = DocumentType.objects.all().order_by("id")
    filter_backends = [DjangoFilterBackend]
    filterset_class = DocumentTypeFilter
    pagination_class = DocumentTypePagination

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def destroy(self, request, pk=None):
        instance = self.get_object()
        if request.user.is_owner:
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        
        return Response(
            {"message": "No tiene permisos para realizar esta accion"},
            status=status.HTTP_403_FORBIDDEN,
        )