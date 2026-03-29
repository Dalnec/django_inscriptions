from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from .managers import UserManager

# Create your models here.


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
    # GENDER_CHOICES = (
    #     ('M', 'Masculino'),
    #     ('F', 'Femenino'),
    # )

    username = models.CharField(max_length=11, unique=True)
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

    def save(self, **kwargs):
        self.username = self.username.upper()
        # self.names = self.names.upper()
        # self.lastname = self.lastname.upper()
        super(User, self).save()

    class Meta:
        verbose_name_plural = "Usuarios"
        db_table = "User"
        ordering = ["-id"]

    def __str__(self):
        return f"{self.names}-{self.lastname}"
