from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


def home(request):
    """Home page - redirects to login or dashboard"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    return redirect('login')


@login_required
def dashboard(request):
    """Main dashboard - different views based on user role"""
    context = {
        'user': request.user,
    }
    
    if request.user.is_patient():
        # Patient dashboard
        patient = request.user.patient_profile
        from treatments.models import Treatment, MedicalOrder
        
        treatments = Treatment.objects.filter(patient=patient).order_by('-created_at')[:5]
        recent_orders = MedicalOrder.objects.filter(treatment__patient=patient).order_by('-created_at')[:5]
        
        context.update({
            'patient': patient,
            'treatments': treatments,
            'recent_orders': recent_orders,
        })
        return render(request, 'core/dashboard_patient.html', context)
    
    elif request.user.is_doctor():
        # Doctor dashboard
        from patients.models import Patient
        from treatments.models import Treatment
        
        if request.user.is_medical_director():
            patients = Patient.objects.all()[:10]
            treatments = Treatment.objects.all().order_by('-created_at')[:10]
        else:
            treatments = Treatment.objects.filter(doctor=request.user).order_by('-created_at')[:10]
            patient_ids = treatments.values_list('patient_id', flat=True).distinct()
            patients = Patient.objects.filter(id__in=patient_ids)[:10]
        
        context.update({
            'patients': patients,
            'treatments': treatments,
        })
        return render(request, 'core/dashboard_doctor.html', context)
    
    elif request.user.is_lab_operator():
        # Lab operator dashboard
        from laboratory.models import Puncture, Oocyte, Embryo
        
        recent_punctures = Puncture.objects.all().order_by('-created_at')[:10]
        pending_oocytes = Oocyte.objects.filter(current_state__in=['VERY_IMMATURE', 'IMMATURE', 'MATURE']).count()
        developing_embryos = Embryo.objects.filter(current_state='DEVELOPING').count()
        
        context.update({
            'recent_punctures': recent_punctures,
            'pending_oocytes': pending_oocytes,
            'developing_embryos': developing_embryos,
        })
        return render(request, 'core/dashboard_lab.html', context)
    
    elif request.user.is_admin():
        # Admin dashboard
        from users.models import User
        from patients.models import Patient
        from treatments.models import Treatment
        
        total_users = User.objects.count()
        total_patients = Patient.objects.count()
        active_treatments = Treatment.objects.filter(status='ACTIVE').count()
        
        context.update({
            'total_users': total_users,
            'total_patients': total_patients,
            'active_treatments': active_treatments,
        })
        return render(request, 'core/dashboard_admin.html', context)
    
    return render(request, 'core/dashboard.html', context)


@login_required
def appointments_placeholder(request):
    """Placeholder for appointments module (external API)"""
    return render(request, 'core/appointments_placeholder.html')


@login_required
def calendar_placeholder(request):
    """Placeholder for calendar module (external API)"""
    return render(request, 'core/calendar_placeholder.html')


@login_required
def payments_placeholder(request):
    """Placeholder for payments module (external API)"""
    return render(request, 'core/payments_placeholder.html')


@login_required
def notifications_placeholder(request):
    """Placeholder for notifications module (external API)"""
    return render(request, 'core/notifications_placeholder.html')


@login_required
def patient_treatments(request):
    """Redirect to patient treatments"""
    if not request.user.is_patient():
        return redirect('dashboard')
    return redirect('my_treatments')


@login_required
def patient_orders(request):
    """Redirect to patient orders"""
    if not request.user.is_patient():
        return redirect('dashboard')
    return redirect('my_orders')
