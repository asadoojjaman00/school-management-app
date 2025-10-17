from django.shortcuts import render,redirect
from .forms import UserRegistrationForm,UserProfileCreation,UserLoginForm
from django.contrib.auth import login,logout
from django.contrib import messages
from .models import User
from .utils import verify_otp,resend_otp



# register view function : 
def register_view(request):
    
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.is_active = False
            user.username = user.email.split('@')[0] + str(User.objects.count() + 1)
            user.save()
            messages.success(request, "Account created please verify your email.")
            
            if not user.is_active:
                verify_otp_view(user,user.id)
                request.session['pending email'] = user.email
                return redirect('verify_otp_page', user_id = user.id)
            
        

    else:
        user_form = UserRegistrationForm()
    return render(request, 'register.html', {'user_form': user_form})




# otp verification view function: 
def verify_otp_view(request, user_id):
    user = User.objects.get(id=user_id)
    if request.method == 'POST':
        otp = request.POST.get('otp')
        result = verify_otp(user, otp)
        if result.error:   # 🔴 এই লাইনেই error!
            messages.error(request, result.error)
        else:
            messages.success(request, "OTP verified successfully!")
            return redirect('login')
    return render(request, 'verify_otp.html')
 





# login view function : 
def login_view(request):
    if request.method == 'POST':
        login_form = UserLoginForm(request.POST)
        if login_form.is_valid():
            user = login_form.cleaned_data['user']

            if not user.is_active:
                verify_otp_view(user)
                request.session['pending email'] = user.email
                return redirect('verify_otp_page', user_id = user.id)
            
        login(request, user)
        return redirect('userProfile')
    else:
        login_form = UserLoginForm()
    return render(request, 'login.html', {'login_form': login_form})


# userprofile view function : 

def userProfile_view(request):
    profile = request.User.UserProfile
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