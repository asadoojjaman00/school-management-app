from django.shortcuts import render,redirect
from .forms import UserRegistrationForm,UserProfileCreation
# from django.contrib.auth import login
from .otpmodels import verify_otp, generate_otp, EmailOTP
from django.contrib import messages
from .models import User
from django.core.mail import send_mail

# register view function : 
def register_view(request):
    
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.is_active = False
            user.username = user.email.split('@')[0] + str(User.objects.count() + 1)
            user.save()
            
            otp = generate_otp()
            EmailOTP.objects.create(user=user, otp=otp)

            send_mail(
                subject=f"{user.full_name} your OTP is here",
                message=f"otp : {otp} don't share anyone",
                from_email='asadoojjaman.cse@gmail.com',
                recipient_list=[user.email],
                fail_silently=True
            )
            messages.success(request, "Account created please verify your email.")
            return redirect('verify_otp_page', user_id=user.id)

    else:
        user_form = UserRegistrationForm()
    return render(request, 'register.html', {'user_form': user_form})




# otp verification view function: 
def verify_otp_view(request, user_id):
    user = User.objects.get(id=user_id)

    if request.method == 'POST':
        otp = request.POST.get('otp')
        success, message =verify_otp(user,otp)
        if success:
            messages.success(request, message)
            return redirect('profile.html')
        else:
            message.error(request, message)

    return render(request, 'verifyOTP.html', {'user':user}) 





# # login view function : 
# def login_view(request):
#     return render(request, 'login.html')


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

 