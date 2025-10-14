from django.contrib.auth.models import AbstractUser , PermissionsMixin
from .managers import UserManager
from django.db import models
from django.utils.translation import gettext_lazy as _ 
import base64
from django.core.files.base import ContentFile


# custom user model section : 

class User(AbstractUser, PermissionsMixin):

    full_name = models.CharField(max_length=255)

    username = models.CharField(
        _("username"),
        max_length=40,
        unique=True,
        db_index=True,
        error_messages={
            "unique": _("A user with that username already exist")
        }
    )

    email = models.EmailField(
        max_length=250,
        unique=True,
        error_messages={
            "unique": _("A user with that email already exist ")
        }
    )
    date_of_birth = models.DateField(null=True, blank=True)
    GENDER_CHOICE= [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    ]

    gender = models.CharField(
        max_length=1,
        choices= GENDER_CHOICE,
        null= True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now_add=False ,auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    def __str__(self):
        return self.email
    
    class Meta:
        indexes = [
            models.Index(fields=['username']),
        ] 
    
    def has_perm(self, perm, obj=None):
        return True
    
    def has_module_perms(self, app_label):
        return True
    
    @property
    def is_staff(self):
        return self.is_admin
    


# user profile model section : 

class UserProfile(User, models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    DEPARTMENT_CHOICE=[
        ('cst', 'CST'),
        ('civil', 'CIVIL'),
        ('eee', 'EEE'),
        ('aidt', 'AIDT'),
    ]

    department = models.CharField(
        max_length=6,
        choices=DEPARTMENT_CHOICE,
        null=True,
        blank=True
    )
    board_roll = models.CharField(max_length=6, unique=True, null=True, blank=False)
    regi_number = models.CharField(max_length=10, unique=True, null=True, blank=True)
    SHIFT_CHOICE =[
        ('M', 'morning'),
        ('D', 'day'),
    ]
    shif = models.CharField(max_length=1,choices=SHIFT_CHOICE, null=True, blank=True)

    image = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    image_base64 = models.TextField(blank=True, null= True)

    def save(self, *args, **kwargs):
        if self.image_base64:
            format, imgstr = self.image_base64.split('; base64,')
            ext = format.split('/')[-1]
            self.image = ContentFile(base64.b64encode(imgstr), name=f"{self.full_name}.{ext}")
            self.image_base64 = None 
        super().save(*args, **kwargs)