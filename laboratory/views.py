from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from treatments.models import Treatment
from .models import Puncture, Oocyte, OocyteStateHistory, Embryo, EmbryoTransfer
from .forms import (
    PunctureForm, OocyteForm, OocyteUpdateForm, 
    EmbryoForm, EmbryoUpdateForm, EmbryoTransferForm
)


@login_required
def puncture_list(request):
    """List all punctures for lab operators"""
    if not request.user.is_lab_operator():
        messages.error(request, 'No tiene permisos para ver esta página.')
        return redirect('dashboard')
    
    punctures = Puncture.objects.all().order_by('-created_at')
    
    return render(request, 'laboratory/puncture_list.html', {'punctures': punctures})


@login_required
def oocyte_list(request):
    """List all oocytes for lab operators"""
    if not request.user.is_lab_operator():
        messages.error(request, 'No tiene permisos para ver esta página.')
        return redirect('dashboard')
    
    oocytes = Oocyte.objects.all().order_by('-created_at')
    
    return render(request, 'laboratory/oocyte_list.html', {'oocytes': oocytes})


@login_required
def embryo_list(request):
    """List all embryos for lab operators"""
    if not request.user.is_lab_operator():
        messages.error(request, 'No tiene permisos para ver esta página.')
        return redirect('dashboard')
    
    embryos = Embryo.objects.all().order_by('-created_at')
    
    return render(request, 'laboratory/embryo_list.html', {'embryos': embryos})


@login_required
def register_puncture(request, treatment_id):
    """Lab operator registers puncture procedure"""
    if not request.user.is_lab_operator():
        messages.error(request, 'Solo los operadores de laboratorio pueden registrar punciones.')
        return redirect('dashboard')
    
    treatment = get_object_or_404(Treatment, id=treatment_id)
    
    if request.method == 'POST':
        form = PunctureForm(request.POST)
        if form.is_valid():
            puncture = form.save(commit=False)
            puncture.treatment = treatment
            puncture.operator = request.user
            puncture.save()
            messages.success(request, 'Punción registrada exitosamente.')
            return redirect('puncture_detail', puncture_id=puncture.id)
    else:
        form = PunctureForm()
    
    return render(request, 'laboratory/register_puncture.html', {
        'treatment': treatment,
        'form': form,
    })


@login_required
def puncture_detail(request, puncture_id):
    """View puncture details and oocytes"""
    if not request.user.is_lab_operator():
        messages.error(request, 'No tiene permisos para ver esta información.')
        return redirect('dashboard')
    
    puncture = get_object_or_404(Puncture, id=puncture_id)
    oocytes = puncture.oocytes.all()
    
    return render(request, 'laboratory/puncture_detail.html', {
        'puncture': puncture,
        'oocytes': oocytes,
    })


@login_required
def add_oocyte(request, puncture_id):
    """Lab operator adds oocyte to puncture"""
    if not request.user.is_lab_operator():
        messages.error(request, 'Solo los operadores de laboratorio pueden agregar óvulos.')
        return redirect('dashboard')
    
    puncture = get_object_or_404(Puncture, id=puncture_id)
    
    if request.method == 'POST':
        form = OocyteForm(request.POST)
        if form.is_valid():
            oocyte = form.save(commit=False)
            oocyte.puncture = puncture
            oocyte.current_state = oocyte.initial_state
            oocyte.save()
            
            # Create state history
            OocyteStateHistory.objects.create(
                oocyte=oocyte,
                from_state='',
                to_state=oocyte.initial_state,
                notes='Estado inicial',
                changed_by=request.user
            )
            
            messages.success(request, 'Óvulo agregado exitosamente.')
            return redirect('puncture_detail', puncture_id=puncture.id)
    else:
        form = OocyteForm()
    
    return render(request, 'laboratory/add_oocyte.html', {
        'puncture': puncture,
        'form': form,
    })


@login_required
def oocyte_detail(request, oocyte_id):
    """View oocyte details and history"""
    if not request.user.is_lab_operator() and not request.user.is_patient():
        messages.error(request, 'No tiene permisos para ver esta información.')
        return redirect('dashboard')
    
    oocyte = get_object_or_404(Oocyte, id=oocyte_id)
    
    # Patients can only see their own oocytes
    if request.user.is_patient():
        if oocyte.puncture.treatment.patient.user != request.user:
            messages.error(request, 'No tiene permisos para ver este óvulo.')
            return redirect('my_biological_products')
    
    state_history = oocyte.state_history.all()
    
    return render(request, 'laboratory/oocyte_detail.html', {
        'oocyte': oocyte,
        'state_history': state_history,
    })


@login_required
def update_oocyte(request, oocyte_id):
    """Lab operator updates oocyte state"""
    if not request.user.is_lab_operator():
        messages.error(request, 'Solo los operadores de laboratorio pueden actualizar óvulos.')
        return redirect('dashboard')
    
    oocyte = get_object_or_404(Oocyte, id=oocyte_id)
    old_state = oocyte.current_state
    
    if request.method == 'POST':
        form = OocyteUpdateForm(request.POST, instance=oocyte)
        if form.is_valid():
            oocyte = form.save()
            
            # Create state history if state changed
            if old_state != oocyte.current_state:
                OocyteStateHistory.objects.create(
                    oocyte=oocyte,
                    from_state=old_state,
                    to_state=oocyte.current_state,
                    notes=f'Actualizado por {request.user.get_full_name()}',
                    changed_by=request.user
                )
            
            messages.success(request, 'Óvulo actualizado exitosamente.')
            return redirect('oocyte_detail', oocyte_id=oocyte.id)
    else:
        form = OocyteUpdateForm(instance=oocyte)
    
    return render(request, 'laboratory/update_oocyte.html', {
        'oocyte': oocyte,
        'form': form,
    })


@login_required
def create_embryo(request, oocyte_id):
    """Lab operator creates embryo from fertilized oocyte"""
    if not request.user.is_lab_operator():
        messages.error(request, 'Solo los operadores de laboratorio pueden crear embriones.')
        return redirect('dashboard')
    
    oocyte = get_object_or_404(Oocyte, id=oocyte_id)
    
    if oocyte.current_state != 'MATURE':
        messages.error(request, 'Solo se pueden fertilizar óvulos maduros.')
        return redirect('oocyte_detail', oocyte_id=oocyte.id)
    
    if request.method == 'POST':
        form = EmbryoForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                embryo = form.save(commit=False)
                embryo.oocyte = oocyte
                embryo.save()
                
                # Update oocyte state
                oocyte.current_state = 'FERTILIZED'
                oocyte.save()
                
                OocyteStateHistory.objects.create(
                    oocyte=oocyte,
                    from_state='MATURE',
                    to_state='FERTILIZED',
                    notes='Fertilizado - Embrión creado',
                    changed_by=request.user
                )
                
                messages.success(request, 'Embrión creado exitosamente.')
                return redirect('embryo_detail', embryo_id=embryo.id)
    else:
        form = EmbryoForm()
    
    return render(request, 'laboratory/create_embryo.html', {
        'oocyte': oocyte,
        'form': form,
    })


@login_required
def embryo_detail(request, embryo_id):
    """View embryo details"""
    if not request.user.is_lab_operator() and not request.user.is_patient():
        messages.error(request, 'No tiene permisos para ver esta información.')
        return redirect('dashboard')
    
    embryo = get_object_or_404(Embryo, id=embryo_id)
    
    # Patients can only see their own embryos
    if request.user.is_patient():
        if embryo.oocyte.puncture.treatment.patient.user != request.user:
            messages.error(request, 'No tiene permisos para ver este embrión.')
            return redirect('my_biological_products')
    
    try:
        transfer = embryo.transfer
    except EmbryoTransfer.DoesNotExist:
        transfer = None
    
    return render(request, 'laboratory/embryo_detail.html', {
        'embryo': embryo,
        'transfer': transfer,
    })


@login_required
def update_embryo(request, embryo_id):
    """Lab operator updates embryo"""
    if not request.user.is_lab_operator():
        messages.error(request, 'Solo los operadores de laboratorio pueden actualizar embriones.')
        return redirect('dashboard')
    
    embryo = get_object_or_404(Embryo, id=embryo_id)
    
    if request.method == 'POST':
        form = EmbryoUpdateForm(request.POST, instance=embryo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Embrión actualizado exitosamente.')
            return redirect('embryo_detail', embryo_id=embryo.id)
    else:
        form = EmbryoUpdateForm(instance=embryo)
    
    return render(request, 'laboratory/update_embryo.html', {
        'embryo': embryo,
        'form': form,
    })


@login_required
def schedule_transfer(request, embryo_id):
    """Lab operator schedules embryo transfer"""
    if not request.user.is_lab_operator():
        messages.error(request, 'Solo los operadores de laboratorio pueden programar transferencias.')
        return redirect('dashboard')
    
    embryo = get_object_or_404(Embryo, id=embryo_id)
    
    if request.method == 'POST':
        form = EmbryoTransferForm(request.POST)
        if form.is_valid():
            transfer = form.save(commit=False)
            transfer.embryo = embryo
            transfer.save()
            
            # Update embryo state if transfer was performed
            if transfer.performed_date:
                embryo.current_state = 'TRANSFERRED'
                embryo.save()
            
            messages.success(request, 'Transferencia programada exitosamente.')
            return redirect('embryo_detail', embryo_id=embryo.id)
    else:
        try:
            transfer = embryo.transfer
            form = EmbryoTransferForm(instance=transfer)
        except EmbryoTransfer.DoesNotExist:
            form = EmbryoTransferForm()
    
    return render(request, 'laboratory/schedule_transfer.html', {
        'embryo': embryo,
        'form': form,
    })


@login_required
def my_biological_products(request):
    """Patient views their cryopreserved oocytes and embryos"""
    if not request.user.is_patient():
        messages.error(request, 'Esta página es solo para pacientes.')
        return redirect('dashboard')
    
    patient = request.user.patient_profile
    
    # Get all punctures for this patient
    from treatments.models import Treatment
    treatments = Treatment.objects.filter(patient=patient)
    punctures = Puncture.objects.filter(treatment__in=treatments)
    
    # Get cryopreserved oocytes
    oocytes = Oocyte.objects.filter(
        puncture__in=punctures,
        current_state='CRYOPRESERVED'
    )
    
    # Get cryopreserved embryos
    embryos = Embryo.objects.filter(
        oocyte__puncture__in=punctures,
        current_state='CRYOPRESERVED'
    )
    
    return render(request, 'laboratory/my_biological_products.html', {
        'oocytes': oocytes,
        'embryos': embryos,
    })
