from django.contrib.auth.models import update_last_login
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import generics, status, viewsets
from rest_framework.decorators import action

# Import for Token
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.user.filters import UserFilter, UserPagination

from .models import Profile, User
from .serializer import (
    CustomTokenSerializer,
    PasswordSerializer,
    ProfileSerializer,
    UserLogin,
    UserSerializer,
)


@extend_schema(tags=["User"])
class UserView(viewsets.ModelViewSet):
    queryset = User.objects.all().exclude(is_superuser=True)
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = UserFilter
    pagination_class = UserPagination

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        user = User.objects.get(id=pk)
        serializer = UserSerializer(user, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors)

    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        user.is_active = not user.is_active
        user.save()
        return Response({"Estado": user.is_active}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["put"], serializer_class=PasswordSerializer)
    def change_password(self, request, pk=None):
        user = self.get_object()
        serializer = PasswordSerializer(data=request.data)
        if serializer.is_valid():
            password = serializer.validated_data["password"]
            password2 = serializer.validated_data["password2"]
            if password == password2:
                user.set_password(password)
                user.save()
                return Response(
                    {"Estado": "Se cambio la contraseña correctamente."},
                    status=status.HTTP_200_OK,
                )
            return Response(
                {"error": "Las contraseñas no coinciden."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=["Profile"])
class ProfileView(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def destroy(self, request, *args, **kwargs):
        profile = self.get_object()
        users = User.objects.filter(profile=profile)
        if users:
            return Response(
                {"error": "El perfil ya fue asignado a un usuario."},
                status=status.HTTP_409_CONFLICT,
            )
        profile.delete()
        return Response(
            {"Estado": "Se elimino Correctamente."}, status=status.HTTP_200_OK
        )


class Login(TokenObtainPairView):
    serializer_class = CustomTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
            user = serializer.user

            # Actualizamos último login
            update_last_login(None, user)

            # Serializamos la respuesta con los datos de UserLogin que mejoramos antes
            user_data = UserLogin(user).data

            return Response(
                {
                    "token": serializer.validated_data.get("access"),
                    "user": user_data,
                },
                status=status.HTTP_200_OK,
            )

        except Exception:
            return Response(
                {"error": "Credenciales inválidas para este evento."},
                status=status.HTTP_400_BAD_REQUEST,
            )


class Logout(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        user = User.objects.filter(id=request.data.get("user", 0))
        if user.exists():
            RefreshToken.for_user(user.first())
            return Response(
                {"message": "Sesión cerrada correctamente."}, status=status.HTTP_200_OK
            )
        return Response(
            {"error": "No existe este usuario."}, status=status.HTTP_400_BAD_REQUEST
        )
