from rest_framework import generics, viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema
from django_filters.rest_framework import DjangoFilterBackend

from .models import *
from .serializers import *
from .filters import *


@extend_schema(tags=["PaymentMethod"])
class PaymentMethodView(viewsets.GenericViewSet):
    serializer_class = PaymentMethodSerializer
    queryset = PaymentMethod.objects.all().order_by("id")
    filter_backends = [DjangoFilterBackend]
    filterset_class = PaymentMethodFilter
    pagination_class = PaymentMethodPagination

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

@extend_schema(tags=["Tarifa"])
class TarifaView(viewsets.GenericViewSet):
    serializer_class = TarifaSerializer
    queryset = Tarifa.objects.all().order_by("id")
    filter_backends = [DjangoFilterBackend]
    filterset_class = TarifaFilter
    pagination_class = TarifaPagination

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

@extend_schema(tags=["Inscription"])
class InscriptionView(viewsets.GenericViewSet):
    serializer_class = InscriptionSerializer
    queryset = Inscription.objects.all().order_by("id")
    filter_backends = [DjangoFilterBackend]
    filterset_class = InscriptionFilter
    pagination_class = InscriptionPagination

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

@extend_schema(tags=["InscriptionGroup"])
class InscriptionGroupView(viewsets.ModelViewSet):
    queryset = InscriptionGroup.objects.all()
    serializer_class = InscriptionGroupCreateSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = InscriptionGroupFilter
    # permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'], url_path='register-group')
    def register_group(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            group = serializer.save()
            return Response({"message": "Grupo registrado con éxito", "group_id": group.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)