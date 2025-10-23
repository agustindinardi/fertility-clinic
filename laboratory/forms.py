from django import forms
from .models import Puncture, Oocyte, Embryo, EmbryoTransfer


class PunctureForm(forms.ModelForm):
    """Form for registering puncture procedure"""
    
    class Meta:
        model = Puncture
        fields = ['date', 'operating_room', 'complications']
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'complications': forms.Textarea(attrs={'rows': 3}),
        }


class OocyteForm(forms.ModelForm):
    """Form for registering oocyte"""
    
    class Meta:
        model = Oocyte
        fields = ['oocyte_id', 'initial_state']


class OocyteUpdateForm(forms.ModelForm):
    """Form for updating oocyte state"""
    
    class Meta:
        model = Oocyte
        fields = ['current_state', 'maturation_time', 'discard_reason', 'nitrogen_tube', 'rack_number']
        widgets = {
            'discard_reason': forms.Textarea(attrs={'rows': 2}),
        }


class EmbryoForm(forms.ModelForm):
    """Form for creating embryo from fertilization"""
    
    class Meta:
        model = Embryo
        fields = ['embryo_id', 'fertilization_technique', 'sperm_source', 'quality']


class EmbryoUpdateForm(forms.ModelForm):
    """Form for updating embryo"""
    
    class Meta:
        model = Embryo
        fields = ['current_state', 'pgt_performed', 'pgt_result', 'nitrogen_tube', 'rack_number', 'discard_reason']
        widgets = {
            'discard_reason': forms.Textarea(attrs={'rows': 2}),
        }


class EmbryoTransferForm(forms.ModelForm):
    """Form for scheduling/recording embryo transfer"""
    
    class Meta:
        model = EmbryoTransfer
        fields = ['scheduled_date', 'performed_date', 'beta_positive', 'gestational_sac', 
                  'clinical_pregnancy', 'live_birth', 'notes']
        widgets = {
            'scheduled_date': forms.DateInput(attrs={'type': 'date'}),
            'performed_date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }
