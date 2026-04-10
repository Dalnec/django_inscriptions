from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.exceptions import ValidationError
from django.db import models

from .managers import UserManager


class Profile(models.Model):
    description = models.CharField(max_length=30, blank=True)
    state = models.BooleanField(default=True)

    def save(self, **kwargs):
        self.description = self.description.upper()
        super(Profile, self).save()

    class Meta:
        verbose_name_plural = "Perfiles"
        db_table = "Profile"

    def __str__(self):
        return f"{self.description}"


class User(AbstractBaseUser, PermissionsMixin):
    # Este es el que Django usa para el login (debe ser único)
    # Formato interno: "SHORTNAME_USERNAME"
    username = models.CharField(max_length=50, unique=True)
    # Este es lo que el usuario escribe en el formulario
    login_name = models.CharField(
        max_length=11, verbose_name="Nombre de usuario", null=True, blank=True
    )
    names = models.CharField(max_length=30, null=True, blank=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    lastname = models.CharField(max_length=30, null=True, blank=True)
    # gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, default='M')
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="profile",
        related_name="profile_description",
    )
    activity = models.ForeignKey(
        "activity.Activity",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="activity",
        related_name="activities",
    )
    permissions = models.JSONField(null=True, blank=True)

    USERNAME_FIELD = "username"  # especificamos el campo que servirá como nombre de usuario para el login
    REQUIRED_FIELDS = [
        "email"
    ]  # es posible agregar mas campos obligatorios para la creacion de usuarios

    objects = UserManager()

    def save(self, *args, **kwargs):
        # Si es superusuario, no le forzamos el prefijo del evento
        if self.is_superuser:
            self.username = self.username.upper()
        else:
            # Lógica normal para usuarios de eventos
            if self.activity and self.login_name:
                self.username = f"{self.activity.shortname}_{self.login_name}".upper()
            else:
                # Esto evita errores si intentas guardar un usuario sin actividad
                # (aunque por lógica de negocio siempre deberían tener una)
                self.username = self.username.upper()

        # Validación de límite de 2 (solo para usuarios normales)
        if not self.pk and not self.is_superuser:
            exists_count = User.objects.filter(
                login_name=self.login_name.upper() if self.login_name else "", 
                activity=self.activity
            ).count()
            if exists_count >= 2:
                raise ValueError("Ya existen 2 usuarios con este nombre en este evento.")

        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Usuarios"
        db_table = "User"
        ordering = ["-id"]

    def __str__(self):
        return (
            f"{self.username} ({self.activity.shortname if self.activity else 'N/A'})"
        )
