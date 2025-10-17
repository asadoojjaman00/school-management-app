from django.urls import path 
from . import views

urlpatterns = [
    path('register/', views.register_view, name="register"),
    path('login/', views.login_view, name="login"),
    path('verify-otp/<int:user_id>/', views.verify_otp_view, name="verify_otp_page"),
    path('profile/', views.userProfile_view, name="userProfile"),
    path('resend-otp/<int:user_id>/', views.resendOTP, name='resendOTP')
]
