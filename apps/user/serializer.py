from rest_framework import exceptions, serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import Profile, User


class PasswordSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)


class UserSerializer(serializers.ModelSerializer):
    profile_description = serializers.ReadOnlyField(source="profile.description")

    class Meta:
        model = User
        fields = (
            "id",
            "names",
            "email",
            "lastname",
            "username",
            "password",
            "is_active",
            "profile",
            "profile_description",
            "permissions",
            "activity",
        )
        extra_kwargs = {"password": {"write_only": True}}


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"


class UserLogin(serializers.ModelSerializer):
    # Traemos la descripción del perfil de forma segura
    profile_description = serializers.ReadOnlyField(
        source="profile.description", default=None
    )
    # Traemos el nombre de la actividad (opcional, pero útil)
    activity_shortname = serializers.ReadOnlyField(
        source="activity.shortname", default=None
    )

    class Meta:
        model = User
        # Seleccionamos solo lo que el frontend realmente necesita
        fields = [
            "id",
            "username",
            "names",
            "lastname",
            "email",
            "profile",
            "profile_description",
            "activity",
            "activity_shortname",
            "permissions",
            "is_staff",
        ]
        # Garantizamos que si alguien intenta usar este serializer para crear,
        # la contraseña nunca se devuelva en el JSON de respuesta.
        extra_kwargs = {"password": {"write_only": True}}


class CustomTokenSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # 1. Obtenemos los datos crudos del request
        username_input = attrs.get("username")
        shortname_input = self.context["request"].data.get("shortname")
        # password = attrs.get("password")

        if not shortname_input:
            raise exceptions.ValidationError(
                "El nombre del evento (shortname) es obligatorio."
            )

        # 2. Construimos el username real (el que está en la DB)
        internal_username = f"{shortname_input}_{username_input}".upper()

        # 3. Reemplazamos en los atributos para que el super().validate funcione
        attrs["username"] = internal_username

        try:
            # Esto llama a authenticate() internamente usando el username compuesto
            data = super().validate(attrs)
        except exceptions.AuthenticationFailed:
            raise exceptions.AuthenticationFailed(
                "Usuario, contraseña o evento incorrectos."
            )

        return data
