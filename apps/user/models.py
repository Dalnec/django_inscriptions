from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from .managers import UserManager
# Create your models here.

class Profile(models.Model):
    description = models.CharField(max_length=30, blank=True)
    state = models.BooleanField(default=True)

    def save(self, **kwargs):
        self.description = self.description.upper()
        super(Profile, self).save()

    class Meta:
        verbose_name_plural = 'Perfiles'
        db_table = 'Profile'

    def __str__(self):
        return f"{self.description}"


class Permission(models.Model):
    description = models.CharField(max_length=30, blank=True, unique=True)
    category = models.CharField(max_length=30, blank=True, null=True, default='')
    ref = models.CharField(max_length=30, blank=True)
    state = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'Permisos'
        db_table = 'Permission'
        ordering = ['-id']

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
        verbose_name='profile',
        related_name='profile_description'
    )
    # permissions = models.ManyToManyField(Permission, through='DetailPermission', related_name ='permissions_detailpermission', blank=True)
    
    USERNAME_FIELD = 'username' #especificamos el campo que servirá como nombre de usuario para el login
    REQUIRED_FIELDS = ['email'] #es posible agregar mas campos obligatorios para la creacion de usuarios
    
    objects = UserManager()
    
    def save(self, **kwargs):
        self.username = self.username.upper()
        # self.names = self.names.upper()
        # self.lastname = self.lastname.upper()
        super(User, self).save()

    class Meta:
        verbose_name_plural = 'Usuarios'
        db_table = 'User'
        ordering = ['-id']
    
    def __str__(self):
        return f"{self.names}-{self.lastname}"


class DetailPermission(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True, 
        null=True,
        verbose_name='user',
        related_name='user_permission'
    )
    permission = models.ForeignKey(
        Permission,
        on_delete=models.CASCADE,
        blank=True, 
        null=True,
        verbose_name='permission',
        related_name='permission_description'
    )
    state = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'Detalles Permisos'
        db_table = 'DetailPermission'

    def __str__(self):
        return f"{self.user}-{self.permission}"
