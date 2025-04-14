# managers.py es una capa de organizacion para poder separar las consultas a la BD de las vistas(views)
from django.db import models
# para poder sobre-escribir la administracion de usuarios django
from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager, models.Manager):
    """
    Clase Managers para la creacion de superusers
    """
    def _create_user(self, username, email, password, is_staff, is_superuser, is_active, **extra_fields):
        """
        Creacion de usuarios
        """
        user = self.model(
            username = username,
            email = email,
            is_staff = is_staff,
            is_superuser = is_superuser,
            is_active = is_active,
            **extra_fields
        )
        user.set_password(password) #encripta la contraseña
        user.save(using=self.db)
        return user
    
    def create_superuser(self, username, email, password=None, **extra_fields):
        """
        Creacion del super usuario
        """
        return self._create_user(username, email, password, True, True, True, **extra_fields)
    
    def create_user(self, username, email, password=None, **extra_fields):
        """
        Crea usuarios no super
        """
        return self._create_user(username, email, password, False, False, True, **extra_fields)
        # return self._create_user(username, email, password, False, False, False, **extra_fields)
    
    def cod_validation(self, id_user, codregistro):
        if self.filter(id=id_user, codregistro=codregistro).exists():
            return True
        else:
            return False
    
    def usuarios_sistema(self):
        return self.filter(
            is_superuser=False
        ).order_by('-last_login')