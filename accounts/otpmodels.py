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
    








"""

email otp send function : 


"""

# from django.core.mail import send_mail

# def send_otp_email(user):
#     otp_entry = EmailOTP.objects.create(user=user)
#     subject = 'Your verification OTP'
#     message = f'Hello {user.full_name}, \nYour OTP is : {otp_entry.otp}\ndon"t share your otp'
#     from_email = 'asadoojjaman.cse@gmail.com'
#     recipient_list = [user.email]
#     send_mail(subject, message, from_email, recipient_list) 
#     return otp_entry




"""

email otp verify function : 


"""


def verify_otp(user,otp):
    try:
        otp_entry = EmailOTP.objects.get(user=user, otp=otp)
        if otp_entry.is_expired():
            return False, "OTP Expired"
        else:
            user.is_active = True
            user.save()
            otp_entry.delete()
            return True, "OTP verification successful" 
    except EmailOTP.DoesNotExist:
        return False, "Invalid OTP"