from django.utils import timezone
from django.db import models
from datetime import timedelta
from .models import User
import random 

def generate_otp():
    return str(random.randint(100000, 999999))


class EmailOTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="email_otp")
    otp = models.CharField(max_length=6, default=generate_otp)
    created_at = models.DateTimeField(auto_now_add=True)
    expiry_time = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.expiry_time:
            self.expiry_time = timezone.now() + timedelta(minutes=2)
        super().save(*args,**kwargs)

    def is_expired(self, *args, **kwargs):
        return timezone.now() > self.expiry_time
    
    def __str__(self):
        return f"{self.user.email} - {self.otp}"
    

