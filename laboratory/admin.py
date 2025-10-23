from django.contrib import admin
from .models import Puncture, Oocyte, OocyteStateHistory, Embryo, EmbryoTransfer


@admin.register(Puncture)
class PunctureAdmin(admin.ModelAdmin):
    list_display = ['treatment', 'date', 'operating_room', 'operator']
    list_filter = ['date']
    search_fields = ['treatment__patient__user__first_name', 'treatment__patient__user__last_name']


@admin.register(Oocyte)
class OocyteAdmin(admin.ModelAdmin):
    list_display = ['oocyte_id', 'puncture', 'initial_state', 'current_state']
    list_filter = ['initial_state', 'current_state']
    search_fields = ['oocyte_id']


@admin.register(OocyteStateHistory)
class OocyteStateHistoryAdmin(admin.ModelAdmin):
    list_display = ['oocyte', 'from_state', 'to_state', 'created_at', 'changed_by']
    list_filter = ['from_state', 'to_state']


@admin.register(Embryo)
class EmbryoAdmin(admin.ModelAdmin):
    list_display = ['embryo_id', 'quality', 'current_state', 'fertilization_technique', 'pgt_performed']
    list_filter = ['current_state', 'fertilization_technique', 'quality', 'pgt_performed']
    search_fields = ['embryo_id']


@admin.register(EmbryoTransfer)
class EmbryoTransferAdmin(admin.ModelAdmin):
    list_display = ['embryo', 'scheduled_date', 'performed_date', 'beta_positive', 'clinical_pregnancy', 'live_birth']
    list_filter = ['beta_positive', 'clinical_pregnancy', 'live_birth']
