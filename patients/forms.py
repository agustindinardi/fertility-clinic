from django import forms
from .models import Patient, MedicalHistory, Partner


class PatientProfileForm(forms.ModelForm):
    """Form for patients to complete their profile - only patient-specific fields"""
    
    class Meta:
        model = Patient
        fields = ['occupation', 'medical_coverage', 'member_number']


class MedicalHistoryForm(forms.ModelForm):
    """Form for doctors to create/update medical history"""
    
    class Meta:
        model = MedicalHistory
        fields = [
            'clinical_background', 'surgical_background', 'personal_background',
            'family_background', 'gynecological_background', 'physical_exam', 'phenotype'
        ]
        widgets = {
            'clinical_background': forms.Textarea(attrs={'rows': 3}),
            'surgical_background': forms.Textarea(attrs={'rows': 3}),
            'personal_background': forms.Textarea(attrs={'rows': 3}),
            'family_background': forms.Textarea(attrs={'rows': 3}),
            'gynecological_background': forms.Textarea(attrs={'rows': 3}),
            'physical_exam': forms.Textarea(attrs={'rows': 3}),
            'phenotype': forms.Textarea(attrs={'rows': 2}),
        }


class PartnerForm(forms.ModelForm):
    """Form for adding partner information"""
    
    class Meta:
        model = Partner
        fields = ['first_name', 'last_name', 'date_of_birth', 'biological_sex', 'dni', 'genital_background']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'genital_background': forms.Textarea(attrs={'rows': 3}),
        }
