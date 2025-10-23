from django.contrib import admin
from .models import Treatment, MonitoringDay, StudyResult, MedicalOrder, Payment


@admin.register(Treatment)
class TreatmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'patient', 'doctor', 'objective', 'status', 'created_at']
    list_filter = ['status', 'objective']
    search_fields = ['patient__user__first_name', 'patient__user__last_name']


@admin.register(MonitoringDay)
class MonitoringDayAdmin(admin.ModelAdmin):
    list_display = ['treatment', 'date', 'completed']
    list_filter = ['completed', 'date']


@admin.register(StudyResult)
class StudyResultAdmin(admin.ModelAdmin):
    list_display = ['study_name', 'study_type', 'treatment', 'created_at']
    list_filter = ['study_type']


@admin.register(MedicalOrder)
class MedicalOrderAdmin(admin.ModelAdmin):
    list_display = ['order_type', 'treatment', 'created_at']
    list_filter = ['order_type']


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['treatment', 'payer_type', 'amount_due', 'amount_paid', 'balance']
    list_filter = ['payer_type']
