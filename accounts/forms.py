from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User,UserProfile



# user registration form : 

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['full_name', 'email', 'date_of_birth', 'gender','password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email already registered')
        return email
    
# user creation form : 

class UserProfileCreation(forms.ModelForm):
    class Meta:
        mode = UserProfile
        fields = ['department', 'semester', 'board_roll','regi_number', 'shift', 'image']

