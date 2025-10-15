from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User,UserProfile



# user registration form : 

class UserRegistrationForm(UserCreationForm):
    otp = forms.CharField(max_length=6,required=False,label='Enter your otp')
    class Meta:
        mode = User
        fields = ['full_name', 'email', 'date_of_birth', 'gender','password1', 'password2']

# user creation form : 

class UserProfileCreation(forms.ModelForm):
    class Meta:
        mode = UserProfile
        fields = ['department', 'semester', 'board_roll','regi_number', 'shift', 'image']

