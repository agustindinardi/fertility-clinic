from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from patients.models import Patient, MedicalHistory, Partner
from .models import Treatment, MonitoringDay, StudyResult, MedicalOrder
from .forms import (
    TreatmentInitiationForm, MedicalHistoryInlineForm, PartnerInlineForm,
    StudyResultForm, StimulationProtocolForm, MonitoringDayForm, MedicalOrderForm
)


@login_required
def treatment_list(request):
    """View for doctors to see all treatments"""
    if not request.user.is_doctor() and not request.user.is_admin():
        messages.error(request, 'No tiene permisos para ver esta página.')
        return redirect('dashboard')
    
    treatments = Treatment.objects.all().order_by('-created_at')
    
    return render(request, 'treatments/treatment_list.html', {'treatments': treatments})


@login_required
def my_treatments(request):
    """View for patients to see their treatments"""
    if not request.user.is_patient():
        messages.error(request, 'Esta página es solo para pacientes.')
        return redirect('dashboard')
    
    patient = request.user.patient_profile
    treatments = Treatment.objects.filter(patient=patient).order_by('-created_at')
    
    return render(request, 'treatments/my_treatments.html', {'treatments': treatments})


@login_required
def treatment_detail(request, treatment_id):
    """View treatment details"""
    treatment = get_object_or_404(Treatment, id=treatment_id)
    
    # Check permissions
    if request.user.is_patient():
        if treatment.patient.user != request.user:
            messages.error(request, 'No tiene permisos para ver este tratamiento.')
            return redirect('my_treatments')
    elif not request.user.is_doctor() and not request.user.is_lab_operator():
        messages.error(request, 'No tiene permisos para ver este tratamiento.')
        return redirect('dashboard')
    
    monitoring_days = treatment.monitoring_days.all()
    study_results = treatment.study_results.all()
    medical_orders = treatment.medical_orders.all()
    
    return render(request, 'treatments/treatment_detail.html', {
        'treatment': treatment,
        'monitoring_days': monitoring_days,
        'study_results': study_results,
        'medical_orders': medical_orders,
    })


@login_required
def initiate_treatment(request, patient_id):
    """Doctor initiates a new treatment for a patient"""
    if not request.user.is_doctor():
        messages.error(request, 'Solo los médicos pueden iniciar tratamientos.')
        return redirect('dashboard')
    
    patient = get_object_or_404(Patient, id=patient_id)
    
    if request.method == 'POST':
        treatment_form = TreatmentInitiationForm(request.POST)
        
        # Get or create medical history
        try:
            medical_history = patient.medical_history
            history_form = MedicalHistoryInlineForm(request.POST, instance=medical_history)
        except MedicalHistory.DoesNotExist:
            history_form = MedicalHistoryInlineForm(request.POST)
        
        # Partner form (optional)
        try:
            partner = patient.partner
            partner_form = PartnerInlineForm(request.POST, instance=partner)
        except Partner.DoesNotExist:
            partner_form = PartnerInlineForm(request.POST)
        
        if treatment_form.is_valid() and history_form.is_valid():
            with transaction.atomic():
                # Save medical history
                if not hasattr(patient, 'medical_history'):
                    medical_history = history_form.save(commit=False)
                    medical_history.patient = patient
                    medical_history.save()
                else:
                    history_form.save()
                
                # Save partner if data provided
                if partner_form.is_valid() and partner_form.cleaned_data.get('first_name'):
                    if not hasattr(patient, 'partner'):
                        partner = partner_form.save(commit=False)
                        partner.patient = patient
                        partner.save()
                    else:
                        partner_form.save()
                
                # Create treatment
                treatment = treatment_form.save(commit=False)
                treatment.patient = patient
                treatment.doctor = request.user
                treatment.save()
                
                messages.success(request, 'Tratamiento iniciado exitosamente.')
                return redirect('treatment_detail', treatment_id=treatment.id)
    else:
        treatment_form = TreatmentInitiationForm()
        try:
            medical_history = patient.medical_history
            history_form = MedicalHistoryInlineForm(instance=medical_history)
        except MedicalHistory.DoesNotExist:
            history_form = MedicalHistoryInlineForm()
        
        try:
            partner = patient.partner
            partner_form = PartnerInlineForm(instance=partner)
        except Partner.DoesNotExist:
            partner_form = PartnerInlineForm()
    
    return render(request, 'treatments/initiate_treatment.html', {
        'patient': patient,
        'treatment_form': treatment_form,
        'history_form': history_form,
        'partner_form': partner_form,
    })


@login_required
def add_study_result(request, treatment_id):
    """Doctor adds study results to treatment"""
    if not request.user.is_doctor():
        messages.error(request, 'Solo los médicos pueden cargar resultados.')
        return redirect('dashboard')
    
    treatment = get_object_or_404(Treatment, id=treatment_id)
    
    if request.method == 'POST':
        form = StudyResultForm(request.POST, request.FILES)
        if form.is_valid():
            study_result = form.save(commit=False)
            study_result.treatment = treatment
            study_result.save()
            messages.success(request, 'Resultado de estudio agregado exitosamente.')
            return redirect('treatment_detail', treatment_id=treatment.id)
    else:
        form = StudyResultForm()
    
    return render(request, 'treatments/add_study_result.html', {
        'treatment': treatment,
        'form': form,
    })


@login_required
def update_stimulation_protocol(request, treatment_id):
    """Doctor updates stimulation protocol"""
    if not request.user.is_doctor():
        messages.error(request, 'Solo los médicos pueden actualizar el protocolo.')
        return redirect('dashboard')
    
    treatment = get_object_or_404(Treatment, id=treatment_id)
    
    if request.method == 'POST':
        form = StimulationProtocolForm(request.POST, request.FILES, instance=treatment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Protocolo de estimulación actualizado exitosamente.')
            return redirect('treatment_detail', treatment_id=treatment.id)
    else:
        form = StimulationProtocolForm(instance=treatment)
    
    return render(request, 'treatments/update_protocol.html', {
        'treatment': treatment,
        'form': form,
    })


@login_required
def assign_monitoring_days(request, treatment_id):
    """Doctor assigns monitoring days"""
    if not request.user.is_doctor():
        messages.error(request, 'Solo los médicos pueden asignar días de monitoreo.')
        return redirect('dashboard')
    
    treatment = get_object_or_404(Treatment, id=treatment_id)
    
    if request.method == 'POST':
        dates = request.POST.getlist('monitoring_dates')
        for date_str in dates:
            if date_str:
                MonitoringDay.objects.create(treatment=treatment, date=date_str)
        messages.success(request, f'{len(dates)} días de monitoreo asignados exitosamente.')
        return redirect('treatment_detail', treatment_id=treatment.id)
    
    return render(request, 'treatments/assign_monitoring.html', {'treatment': treatment})


@login_required
def create_medical_order(request, treatment_id):
    """Doctor creates medical order"""
    if not request.user.is_doctor():
        messages.error(request, 'Solo los médicos pueden crear órdenes médicas.')
        return redirect('dashboard')
    
    treatment = get_object_or_404(Treatment, id=treatment_id)
    
    if request.method == 'POST':
        form = MedicalOrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.treatment = treatment
            order.save()
            messages.success(request, 'Orden médica creada exitosamente.')
            return redirect('treatment_detail', treatment_id=treatment.id)
    else:
        form = MedicalOrderForm()
    
    return render(request, 'treatments/create_order.html', {
        'treatment': treatment,
        'form': form,
    })


@login_required
def my_orders(request):
    """Patient views their medical orders"""
    if not request.user.is_patient():
        messages.error(request, 'Esta página es solo para pacientes.')
        return redirect('dashboard')
    
    patient = request.user.patient_profile
    orders = MedicalOrder.objects.filter(treatment__patient=patient).order_by('-created_at')
    
    return render(request, 'treatments/my_orders.html', {'orders': orders})
