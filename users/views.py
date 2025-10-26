from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import StaffUserCreationForm, UserUpdateForm
from .forms import PatientRegistrationForm
from .models import User


def login_view(request):
    """User login view"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Bienvenido, {user.get_full_name() or user.username}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos. Por favor, intente nuevamente.')
    
    return render(request, 'users/login.html')


def logout_view(request):
    """User logout view"""
    logout(request)
    messages.info(request, 'Ha cerrado sesión exitosamente.')
    return redirect('login')


def register_view(request):
    """Patient registration view"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = PatientRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'PATIENT'
            user.save()
            
            from patients.models import Patient
            Patient.objects.create(
                user=user,
                occupation=form.cleaned_data.get('occupation', ''),
                medical_coverage=form.cleaned_data.get('medical_coverage', ''),
                member_number=form.cleaned_data.get('member_number', '')
            )
            
            messages.success(request, 'Registro exitoso. Por favor, inicie sesión.')
            return redirect('login')
    else:
        form = PatientRegistrationForm()
    
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile_view(request):
    """User profile view and edit"""
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil actualizado exitosamente.')
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=request.user)
    
    return render(request, 'users/profile.html', {'form': form})


@login_required
def create_staff_user(request):
    """Admin view to create staff users"""
    if not request.user.is_admin():
        messages.error(request, 'No tiene permisos para acceder a esta página.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = StaffUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Usuario {user.username} creado exitosamente.')
            return redirect('manage_users')
    else:
        form = StaffUserCreationForm()
    
    return render(request, 'users/create_staff.html', {'form': form})


@login_required
def manage_users(request):
    """Admin view to manage all users"""
    if not request.user.is_admin():
        messages.error(request, 'No tiene permisos para acceder a esta página.')
        return redirect('dashboard')
    
    users = User.objects.all().order_by('-date_joined')
    return render(request, 'users/manage_users.html', {'users': users})


@login_required
def toggle_user_status(request, user_id):
    """Admin view to activate/deactivate users"""
    if not request.user.is_admin():
        messages.error(request, 'No tiene permisos para realizar esta acción.')
        return redirect('dashboard')
    
    try:
        user = User.objects.get(id=user_id)
        user.is_active = not user.is_active
        user.save()
        status = 'activado' if user.is_active else 'desactivado'
        messages.success(request, f'Usuario {user.username} {status} exitosamente.')
    except User.DoesNotExist:
        messages.error(request, 'Usuario no encontrado.')
    
    return redirect('manage_users')
