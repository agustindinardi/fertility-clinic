from django.contrib import admin
from .models import Patient, MedicalHistory, Partner


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ['get_full_name', 'get_dni', 'get_date_of_birth', 'get_biological_sex', 'medical_coverage_name', 'occupation']
    search_fields = ['user__first_name', 'user__last_name', 'user__dni', 'user__email']
    list_filter = ['user__biological_sex']
    
    def get_full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"
    get_full_name.short_description = 'Nombre Completo'
    
    def get_dni(self, obj):
        return obj.user.dni
    get_dni.short_description = 'DNI'
    get_dni.admin_order_field = 'user__dni'
    
    def get_date_of_birth(self, obj):
        return obj.user.date_of_birth
    get_date_of_birth.short_description = 'Fecha de Nacimiento'
    get_date_of_birth.admin_order_field = 'user__date_of_birth'
    
    def get_biological_sex(self, obj):
        return obj.user.get_biological_sex_display()
    get_biological_sex.short_description = 'Sexo Biológico'
    get_biological_sex.admin_order_field = 'user__biological_sex'


@admin.register(MedicalHistory)
class MedicalHistoryAdmin(admin.ModelAdmin):
    list_display = ['patient', 'created_at', 'updated_at']
    search_fields = ['patient__user__first_name', 'patient__user__last_name']


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'dni', 'patient']
    search_fields = ['first_name', 'last_name', 'dni']
