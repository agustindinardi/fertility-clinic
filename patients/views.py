from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import models
from .models import Patient, MedicalHistory
from .forms import PatientProfileForm


@login_required
def complete_patient_profile(request):
    """View for patients to complete their profile"""
    if not request.user.is_patient():
        messages.error(request, 'Esta página es solo para pacientes.')
        return redirect('dashboard')
    
    patient = request.user.patient_profile
    
    if request.method == 'POST':
        form = PatientProfileForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil completado exitosamente.')
            return redirect('dashboard')
    else:
        form = PatientProfileForm(instance=patient)
    
    return render(request, 'patients/complete_profile.html', {'form': form})


@login_required
def patient_list(request):
    """View for doctors to see their patients"""
    if not request.user.is_doctor() and not request.user.is_lab_operator():
        messages.error(request, 'No tiene permisos para acceder a esta página.')
        return redirect('dashboard')
    
    # Medical directors can see all patients
    if request.user.is_medical_director():
        patients = Patient.objects.all().select_related('user')
    else:
        # Doctors see only their patients (patients with treatments assigned to them)
        from treatments.models import Treatment
        patient_ids = Treatment.objects.filter(doctor=request.user).values_list('patient_id', flat=True).distinct()
        patients = Patient.objects.filter(id__in=patient_ids).select_related('user')
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        patients = patients.filter(
            models.Q(user__first_name__icontains=search_query) |
            models.Q(user__last_name__icontains=search_query) |
            models.Q(dni__icontains=search_query)
        )
    
    return render(request, 'patients/patient_list.html', {
        'patients': patients,
        'search_query': search_query
    })


@login_required
def patient_detail(request, patient_id):
    """View for doctors to see patient details"""
    if not request.user.is_doctor() and not request.user.is_lab_operator():
        messages.error(request, 'No tiene permisos para acceder a esta página.')
        return redirect('dashboard')
    
    patient = get_object_or_404(Patient, id=patient_id)
    
    # Check permissions (medical directors can see all)
    if not request.user.is_medical_director():
        from treatments.models import Treatment
        if not Treatment.objects.filter(patient=patient, doctor=request.user).exists():
            messages.error(request, 'No tiene permisos para ver este paciente.')
            return redirect('patient_list')
    
    try:
        medical_history = patient.medical_history
    except MedicalHistory.DoesNotExist:
        medical_history = None
    
    try:
        partner = patient.partner
    except:
        partner = None
    
    from treatments.models import Treatment
    treatments = Treatment.objects.filter(patient=patient).order_by('-created_at')
    
    return render(request, 'patients/patient_detail.html', {
        'patient': patient,
        'medical_history': medical_history,
        'partner': partner,
        'treatments': treatments
    })
