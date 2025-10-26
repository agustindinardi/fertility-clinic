from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class PatientRegistrationForm(UserCreationForm):
    """Form for patient self-registration with all required fields"""
    occupation = forms.CharField(
        max_length=100,
        required=False,
        label='Ocupación',
        widget=forms.TextInput(attrs={'placeholder': 'Ej: Ingeniero, Docente, etc.'})
    )
    medical_coverage = forms.CharField(
        max_length=100,
        required=False,
        label='Cobertura Médica',
        widget=forms.TextInput(attrs={'placeholder': 'Ej: OSDE, Swiss Medical, etc.'})
    )
    member_number = forms.CharField(
        max_length=50,
        required=False,
        label='Número de Socio',
        widget=forms.TextInput(attrs={'placeholder': 'Número de afiliado'})
    )
    
    class Meta:
        model = User
        fields = [
            'username', 'email', 'first_name', 'last_name', 
            'phone', 'dni', 'biological_sex', 'date_of_birth',
            'password1', 'password2'
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': 'Elija un nombre de usuario'})
        self.fields['email'].widget.attrs.update({'placeholder': 'correo@ejemplo.com'})
        self.fields['first_name'].widget.attrs.update({'placeholder': 'Nombre'})
        self.fields['last_name'].widget.attrs.update({'placeholder': 'Apellido'})
        self.fields['phone'].widget.attrs.update({'placeholder': '11-1234-5678'})
        self.fields['dni'].widget.attrs.update({'placeholder': '12345678'})
        self.fields['password1'].widget.attrs.update({'placeholder': 'Mínimo 8 caracteres'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Repita la contraseña'})


class StaffUserCreationForm(UserCreationForm):
    """Form for admin to create staff users (doctors, lab operators)"""
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'phone', 'dni', 'biological_sex', 'date_of_birth', 'role', 'password1','password2']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }
    
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
        fields = ['first_name', 'last_name', 'email', 'phone', 'dni', 'biological_sex', 'date_of_birth']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }