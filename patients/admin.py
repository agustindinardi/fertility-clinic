from django.contrib import admin
from .models import Patient, MedicalHistory, Partner


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ['user', 'dni', 'date_of_birth', 'biological_sex', 'medical_coverage']
    search_fields = ['user__first_name', 'user__last_name', 'dni']
    list_filter = ['biological_sex', 'medical_coverage']


@admin.register(MedicalHistory)
class MedicalHistoryAdmin(admin.ModelAdmin):
    list_display = ['patient', 'created_at', 'updated_at']
    search_fields = ['patient__user__first_name', 'patient__user__last_name']


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'dni', 'patient']
    search_fields = ['first_name', 'last_name', 'dni']
