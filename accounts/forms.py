from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User,UserProfile
from django.contrib.auth import authenticate


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

# user login form : 

class UserLoginForm(forms.Form):
    email = forms.EmailField(label='email')
    password = forms.CharField(widget=forms.PasswordInput,label='password')

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        user = authenticate(email=email, password=password)

        if not user:
            raise forms.ValidationError('email or password wrong')
        if not user.is_active:
            raise forms.ValidationError('please verify your email than login')
        cleaned_data['user'] = user
        return cleaned_data        