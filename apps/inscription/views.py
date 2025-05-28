import re
from rest_framework import generics, viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema
from django_filters.rest_framework import DjangoFilterBackend
from apps.inscription.functions import send_voucher_email
from django.db import transaction

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
    queryset = Inscription.objects.all().order_by("-id")
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
        if request.user.perfil.descripcion.toUpper() == "Administrador".toUpper():
            instance.delete()
            return Response({"message": "Inscripcion eliminada con exito"}, status=status.HTTP_200_OK)
        
        return Response(
            {"message": "No tiene permisos para realizar esta accion"},
            status=status.HTTP_403_FORBIDDEN,
        )
    
    @action(detail=True, methods=['post'], serializer_class=InscriptionSendEmailSerializer, url_path='send-email')
    def send_email(self, request, pk=None, *args, **kwargs):
        instance = self.get_object()
        email = request.data.get('email', None)
        if not email:
            return Response({"message": "El campo email es requerido"}, status=status.HTTP_400_BAD_REQUEST)

        # Validación con regex
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return Response( {"error": "El formato del correo es inválido"}, status=status.HTTP_400_BAD_REQUEST )
        
        group = instance.group
        send_voucher_email(group, [email])
        return Response({"message": "Correo enviado con exito"}, status=status.HTTP_200_OK)
    

@extend_schema(tags=["InscriptionGroup"])
class InscriptionGroupView(viewsets.ModelViewSet):
    queryset = InscriptionGroup.objects.all().order_by("-id")
    serializer_class = InscriptionGroupCreateSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = InscriptionGroupFilter
    # permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'], url_path='register-group')
    def register_group(self, request):
        try:
            with transaction.atomic():
                serializer = self.get_serializer(data=request.data)
                if serializer.is_valid():
                    group = serializer.save( vouchergroup=self.generate_code() )
                    if group.activity.send_email and group.activity.emails:
                            send_voucher_email(group, group.activity.emails)
                    return Response({"message": "Grupo registrado con éxito", "group_id": group.id}, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=True, methods=['get'])
    def send_email(self, request, pk=None):
        instance = self.get_object()
        # serializer = self.get_serializer(data=request.data)
        # if serializer.is_valid():
        #     data = serializer.validated_data
        #     inscription = Inscription.objects.get(id=data['inscription_id'])
        #     inscription.send_email()
        #     return Response({"message": "Email enviado con éxito"}, status=status.HTTP_200_OK)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        if instance.activity.send_email:
            if not instance.activity.emails:
                return Response({"message": "No hay correos configurados para enviar el voucher"}, status=status.HTTP_400_BAD_REQUEST)
            send_voucher_email(instance, instance.activity.emails)
        return Response({"message": "Email enviado con éxito"}, status=status.HTTP_200_OK)

    def generate_code(self):
        latest = InscriptionGroup.objects.all().order_by('-id').first()
        next_number = latest.id if latest else 1
        return f"G{next_number:04d}"