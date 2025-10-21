from django.core.mail import send_mail
from .otpmodels import EmailOTP
# from decouple import config

def send_otp_email(user):
    otp_entry = EmailOTP.objects.create(user=user)
    subject = 'Your verification OTP'
    message = f'Hello {user.full_name}, \nYour OTP is : {otp_entry.otp}\ndon"t share your otp'
    from_email = 'gmail--hide'
    recipient_list = [user.email]
    send_mail(subject, message, from_email, recipient_list) 
    return otp_entry


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
    

def resend_otp(user):
    existing_otp = EmailOTP.objects.filter(user=user).order_by('created_at').first()
    if existing_otp:
        if existing_otp.is_expired():
            existing_otp.delete()
            send_otp_email(user)
            return True, "new otp sent your email"
        else:
            return False, "your previous is still valid , please check your inbox"
    else:
        send_otp_email(user)
        return True, "otp sent your email"

