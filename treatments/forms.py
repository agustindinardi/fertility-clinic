from django import forms
from .models import Treatment, MonitoringDay, StudyResult, MedicalOrder
from patients.models import MedicalHistory, Partner


class TreatmentInitiationForm(forms.ModelForm):
    """Form for doctors to initiate a new treatment"""
    
    class Meta:
        model = Treatment
        fields = ['objective']


class MedicalHistoryInlineForm(forms.ModelForm):
    """Inline form for medical history during treatment initiation"""
    
    class Meta:
        model = MedicalHistory
        fields = [
            'clinical_background', 'surgical_background', 'personal_background',
            'family_background', 'gynecological_background', 'physical_exam', 'phenotype'
        ]
        widgets = {
            'clinical_background': forms.Textarea(attrs={'rows': 2}),
            'surgical_background': forms.Textarea(attrs={'rows': 2}),
            'personal_background': forms.Textarea(attrs={'rows': 2}),
            'family_background': forms.Textarea(attrs={'rows': 2}),
            'gynecological_background': forms.Textarea(attrs={'rows': 2}),
            'physical_exam': forms.Textarea(attrs={'rows': 2}),
            'phenotype': forms.Textarea(attrs={'rows': 1}),
        }


class PartnerInlineForm(forms.ModelForm):
    """Inline form for partner information"""
    
    class Meta:
        model = Partner
        fields = ['first_name', 'last_name', 'date_of_birth', 'biological_sex', 'dni', 'genital_background']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'genital_background': forms.Textarea(attrs={'rows': 2}),
        }


class StudyResultForm(forms.ModelForm):
    """Form for uploading study results"""
    
    class Meta:
        model = StudyResult
        fields = ['study_type', 'study_name', 'result_file', 'result_text']
        widgets = {
            'result_text': forms.Textarea(attrs={'rows': 3}),
        }


class StimulationProtocolForm(forms.ModelForm):
    """Form for defining stimulation protocol"""
    
    class Meta:
        model = Treatment
        fields = ['stimulation_protocol', 'medication_type', 'medication_dose', 'medication_duration', 
                  'oocytes_viable', 'sperm_viable', 'consent_document']
        widgets = {
            'stimulation_protocol': forms.Textarea(attrs={'rows': 3}),
        }


class MonitoringDayForm(forms.ModelForm):
    """Form for adding monitoring day notes"""
    
    class Meta:
        model = MonitoringDay
        fields = ['notes', 'completed']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
        }


class MedicalOrderForm(forms.ModelForm):
    """Form for creating medical orders"""
    
    class Meta:
        model = MedicalOrder
        fields = ['order_type', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }
