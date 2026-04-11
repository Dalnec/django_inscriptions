from django.contrib.auth import authenticate
from rest_framework import exceptions, serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import Profile, User


class PasswordSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)


class UserSerializer(serializers.ModelSerializer):
    profile_description = serializers.ReadOnlyField(
        source="profile.description", default=None
    )

    # Declaramos login_name como read_only ya que lo generamos nosotros
    login_name = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = (
            "id",
            "names",
            "email",
            "lastname",
            "username",  # El front envía aquí el nombre sencillo
            "login_name",
            "password",
            "is_active",
            "profile",
            "profile_description",
            "permissions",
            "activity",
            "is_staff",
        )
        extra_kwargs = {
            "password": {"read_only": True},  # Cambiado a write_only por seguridad
        }

    def create(self, validated_data):
        """
        Sobrescribimos la creación para mover el valor del 'username'
        del frontend al campo 'login_name' del modelo.
        """
        # 1. Extraemos el nombre que envió el front (ej: "JUAN123")
        plain_username = validated_data.get("username")

        # 2. Lo asignamos a login_name (el campo que no envía el front)
        validated_data["login_name"] = plain_username

        # 3. Extraemos el password para usar create_user (que lo hashea)
        password = validated_data.pop("password", None)

        # 4. Creamos la instancia. El método save() del modelo se encargará
        # de unir el shortname de la actividad + login_name
        user = User(**validated_data)

        if password:
            user.set_password(password)

        user.save()
        return user


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
        username_input = attrs.get("username")
        password = attrs.get("password")
        shortname_input = self.context["request"].data.get("shortname")

        # 1. Intentar autenticación como Superusuario primero (o usuario global)
        # El superusuario no lleva prefijo de shortname
        user = authenticate(username=username_input, password=password)

        if user and user.is_superuser:
            # Si es superusuario, saltamos la lógica del shortname
            self.user = user
            # Generamos los tokens manualmente (lo que hace super().validate internamente)
            refresh = self.get_token(user)
            data = {"refresh": str(refresh), "access": str(refresh.access_token)}
            return data

        # 2. Si no es superusuario, procedemos con la lógica de Evento
        if not shortname_input:
            raise exceptions.ValidationError(
                {"error": "El nombre del evento es requerido."}
            )

        # Construimos el username interno: "EVENTO_USUARIO"
        internal_username = f"{shortname_input}_{username_input}".upper()
        attrs["username"] = internal_username

        try:
            # Llamamos a la lógica estándar de SimpleJWT con el username compuesto
            return super().validate(attrs)
        except exceptions.AuthenticationFailed:
            raise exceptions.AuthenticationFailed(
                "Usuario, contraseña o evento incorrectos."
            )
