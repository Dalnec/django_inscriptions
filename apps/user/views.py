from django.db.models.query_utils import Q
from django.http.response import JsonResponse
from django.contrib.sessions.models import Session
from datetime import datetime
import django_filters

#Import for Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema

from rest_framework import generics, viewsets, status
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializer import (PermissionSerializer, ProfileSerializer, UserLogin,
                        UserSerializer, TokenSerializer)

from .models import DetailPermission, Permission, Profile, User
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import update_last_login
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend

#Paginacion General
class UserPagination(PageNumberPagination):
    page_size = 15
    page_size_query_param = 'page_size'
    max_page_size = 1000

#Vistas de Clientes
class UserFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(label='search',
                                    method='search_data')
    class Meta:
        model = User
        fields = ['search']
    
    def search_data(self, queryset, name, value):
        return queryset.filter(Q(names__icontains=value)|Q(lastname__icontains=value))

@extend_schema(tags=["User"])
class UserView(viewsets.ModelViewSet):
    # permission_classes = (IsAuthenticated,)
    queryset = User.objects.all().exclude(is_superuser=True)
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = UserFilter
    pagination_class = UserPagination
    
    def create(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.create(**serializer.validated_data)
        user.set_password(request.data['password'])
        
        permission = request.data['user_permission']
        for a in permission:
            DetailPermission.objects.create(user=user,
                permission = Permission.objects.get(pk=a))
        user.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request,  pk=None):
        user = User.objects.get(id=pk)
        serializer = UserSerializer(user, data = request.data)
        
        if serializer.is_valid():
            DetailPermission.objects.filter(user=user).delete()
            permission = request.data['user_permission']

            for a in permission:
                DetailPermission.objects.create(user=user,
                permission = Permission.objects.get(pk=a))
            
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors)
    
    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        user.is_active = not user.is_active
        user.save()
        return Response({"Estado": user.is_active}, status=status.HTTP_200_OK)


class ChangePassword(viewsets.ModelViewSet):
    # permission_classes = (IsAuthenticated,)
    queryset = User.objects.all().exclude(is_superuser=True)
    serializer_class = UserSerializer
    
    def update(self, request,  pk=None):
        user = User.objects.get(id=pk)
        user.set_password(request.data['password'])
        user.save()
        return Response({"Password": "Se actuazlizo la clave."}, status=status.HTTP_201_CREATED)


class PermissionView(viewsets.ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer

    def destroy(self, request, *args, **kwargs):
        permission = self.get_object()
        detailper = DetailPermission.objects.filter(permission=permission)
        if detailper:
            return Response({'error': 'El permiso ya fue asignado a un usuario.'}, status=status.HTTP_409_CONFLICT)
        permission.delete()
        return Response({"Estado": "Se elimino Correctamente."}, status=status.HTTP_200_OK)


@extend_schema(tags=["Profile"])
class ProfileView(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def destroy(self, request, *args, **kwargs):
        profile = self.get_object()
        users = User.objects.filter(profile=profile)
        if users:
            return Response({'error': 'El perfil ya fue asignado a un usuario.'}, status=status.HTTP_409_CONFLICT)
        profile.delete()
        return Response({"Estado": "Se elimino Correctamente."}, status=status.HTTP_200_OK)


class Login(TokenObtainPairView):
    serializer_class = TokenSerializer

    def post(self, request, *args, **kwargs):
        username = request.data.get('username', '')
        password = request.data.get('password', '')
        user = authenticate(username=username, password=password)

        if user:
            login_serializer = self.serializer_class(data=request.data)
            if login_serializer.is_valid():
                update_last_login(datetime.now(), user)
                user_serializer = UserLogin(user)
                return Response({
                    'token': login_serializer.validated_data.get('access'),
                    'user': user_serializer.data
                }, status=status.HTTP_200_OK)
            return Response({'error': 'Contraseña o usuario incorrectos.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'Contraseña o usuario incorrectos.'}, status=status.HTTP_400_BAD_REQUEST)


class Logout(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        user = User.objects.filter(id=request.data.get('user', 0))
        if user.exists():
            RefreshToken.for_user(user.first())
            return Response({'message': 'Sesión cerrada correctamente.'}, status=status.HTTP_200_OK)
        return Response({'error': 'No existe este usuario.'}, status=status.HTTP_400_BAD_REQUEST)
