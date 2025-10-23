from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class UserRegistrationForm(UserCreationForm):
    """Form for user registration"""
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'phone', 'password1', 'password2']


class StaffUserCreationForm(UserCreationForm):
    """Form for admin to create staff users (doctors, lab operators)"""
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'phone', 'role', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only allow creating non-patient users
        self.fields['role'].choices = [
            choice for choice in User.ROLE_CHOICES 
            if choice[0] != 'PATIENT'
        ]


class UserUpdateForm(forms.ModelForm):
    """Form for users to update their profile"""
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone']
