from django.shortcuts import render,redirect
from .forms import UserRegistrationForm,UserProfileCreation,UserLoginForm
from django.contrib.auth import login
from django.contrib import messages
from .models import User
from .utils import verify_otp,resend_otp,send_otp_email
from django.db import IntegrityError



# register view function : 
def register_view(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            try:
                user = user_form.save(commit=False)
                user.username = user.email.split('@')[0] + str(User.objects.filter)
                user.is_active = False
                user.save()

                send_otp_email(user)
                messages.success(request, "Account created! Please verify your email.")
                return redirect('verify_otp_page', user_id=user.id)
            except IntegrityError:
                messages.error(request, f"{field.capitalize()}: {error}")

        else:
            # Show all form errors
            for field, errors in user_form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")
    else:
        user_form = UserRegistrationForm()

    return render(request, 'register.html', {'user_form': user_form})


# otp verification view function: 
def verify_otp_view(request, user_id):
    user = User.objects.get(id=user_id)
    if request.method == 'POST':
        otp = request.POST.get('otp')
        success, message = verify_otp(user, otp)
        if not success:   
            messages.error(request, message)
        else:
            messages.success(request, message)
            return redirect('login')
    else:
        return render(request, 'verifyOTP.html', {'user':user})
 









# login view function : 
def login_view(request):
    if request.method == 'POST':
        login_form = UserLoginForm(request.POST)
        if login_form.is_valid():
            user = login_form.user

            if not user.is_active:
                request.session['pending_email'] = user.email
                return redirect('verify_otp_page', user_id = user.id)
            
            login(request, user)
            return redirect('userprofile')
    else:
        login_form = UserLoginForm()
    return render(request, 'login.html', {'login_form':login_form})


# userprofile view function : 

def userProfile_view(request):
    profile = request.User.userprofile
    if request.method == 'POST':
        userProfile = UserProfileCreation(request.POST)
        if userProfile.is_valid():
            userProfile.save()
            return redirect('profile')
    else:
        userProfile = UserProfileCreation(instance=profile)
    return render(request, 'profile.html', {'userProfile':userProfile})


def resendOTP(request, user_id):
    user = User.objects.get(id=user_id)
    success, message = resend_otp(user)
    messages.info(request,message)
    return redirect('verify_otp_page',user_id=user.id)