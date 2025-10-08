from django.db import models
from django.contrib.auth.models import AbstractUser , AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _
# Create your models here.


class UserManager(BaseUserManager):
    def _create_user(self, username, password, full_name, **extra_fields):
        
        if not username:
            raise ValueError("user must have an username")
        
        if not full_name:
            raise ValueError("user must have an fullname")
        
        user = self.model(
            username=username,
            full_name=full_name,
            **extra_fields
        )

        user.set_password(password)
        user.save(using= self._db)
        return user
    
    def create_user(self, username, password=None, full_name= None, **extra_fields):
        extra_fields.setdefault("is_admin", False)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_active", False)
        return self._create_user(self, username, password, full_name, **extra_fields)
    

    def create_superuser(self, username, password=None, full_name=None, **extra_fields):
        extra_fields.setdefault("is_admin", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        if extra_fields.get("is_admin") is not True:
            raise ValueError("superuser must have is_admin=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("superuser must have is_superuser=True.")
        return self._create_user(self, username, password, full_name, **extra_fields)
            





class User(AbstractUser , PermissionsMixin):

    username = models.CharField(
        _("username"),
        max_length= 150,
        unique= True,
        db_index= True,
        error_messages={
            "unique": _("A user with that username already exists.")
        }
    )

    phone = models.CharField(
        blank=True,
        unique=True,
        null=True,
        max_length=20
    )

    email = models.EmailField(
        verbose_name="email address",
        unique=True,
        blank=True,
        null=True,
        error_messages={
            "unique":_("A user with that email already exists.")
        }

    )

    full_name = models.CharField(max_length=225)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active= models.BooleanField(default=False)
    is_verified = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False, editable=False)
    updated_at = models.DateTimeField(auto_now_add=False, auto_now=True, editable=False)

    objects = UserManager()


    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["full_name"]

    def __str__(self):
        return self.username
    
    class Meta:
        indexes = [
            models.Index(fields=['username'])
        ]

        