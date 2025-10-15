from django.shortcuts import render,redirect
from .forms import UserRegistrationForm,UserProfileCreation
from django.contrib.auth import login
from .otpmodels import send_otp_email,verify_otp
from django.contrib import messages
from .models import User


# register view function : 
def register_view(request):

    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        email = request.POST.get('email')

        if 'otp' in request.POST:
            otp = request.POST.get('otp')
            user = User.objects.get(email =email)
            valid, msg= verify_otp(user,otp)

            if valid:
                messages.success(request, msg)
                
        if user_form.is_valid():
            user = user_form.save()
            login(request,user)
            return redirect('profile_edit')
    else:
        user_form - UserRegistrationForm()
    return render(request, 'register.html', {'user_form': user_form})


# login view function : 
def login_view(request):
    return render(request, 'login.html')


# userprofile view function : 

def userProfile_view(request):
    if request.method == 'POST':
        userProfile = UserProfileCreation(request.POST)
        if userProfile.is_valid():
            userProfile.save()
            return redirect('profile')
    else:
        userProfile = UserProfileCreation(instance=profile)
    return render(request, 'profile.html', {'userProfile':userProfile})

