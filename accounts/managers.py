from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _ 
from django.db import models

class UserManager(BaseUserManager):
    

    def _create_user(self, email, full_name, password, **extra_fields):

        if not email:
            raise ValueError("user must have an email")
      
        if not full_name:
            raise ValueError("user must have an full_name")
        

        email = self.normalize_email(email)

        
        
        user = self.model(
            email=email,
            full_name=full_name,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self, email, full_name=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_admin", False)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_active", False)

        return self._create_user(email, full_name, password, **extra_fields)
    
    def create_superuser(self, email, full_name= None, password=None, **extra_fields):

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_admin", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_admin") is not True:
            raise ValueError("superuser must have is_admin = True")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("superuser must have is_superuser = True ")
        
        return self._create_user(email, full_name, password, **extra_fields)