from django.db import models
from django.conf import settings


class Patient(models.Model):
    """
    Patient model - extends User with medical information
    """
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='patient_profile')
    occupation = models.CharField(max_length=100, blank=True)
    medical_coverage_id = models.IntegerField(null=True, blank=True, verbose_name='ID Cobertura Médica')
    medical_coverage_name = models.CharField(max_length=100, blank=True, verbose_name='Nombre Cobertura Médica')
    member_number = models.CharField(max_length=50, blank=True, verbose_name='Número de Socio')
    
    # Medical history will be created when first appointment is made
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.get_full_name()} - DNI: {self.dni}"
    
    class Meta:
        verbose_name = 'Paciente'
        verbose_name_plural = 'Pacientes'


class MedicalHistory(models.Model):
    """
    Medical history for a patient - created on first consultation
    """
    
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE, related_name='medical_history')
    
    # Clinical background
    clinical_background = models.TextField(blank=True, verbose_name='Antecedentes Clínicos')
    surgical_background = models.TextField(blank=True, verbose_name='Antecedentes Quirúrgicos')
    personal_background = models.TextField(blank=True, verbose_name='Antecedentes Personales')
    family_background = models.TextField(blank=True, verbose_name='Antecedentes Familiares')
    
    # Gynecological background (for female patients)
    gynecological_background = models.TextField(blank=True, verbose_name='Antecedentes Ginecológicos')
    
    # Physical exam
    physical_exam = models.TextField(blank=True, verbose_name='Examen Físico')
    phenotype = models.TextField(blank=True, verbose_name='Fenotipo')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Historia Clínica - {self.patient}"
    
    class Meta:
        verbose_name = 'Historia Clínica'
        verbose_name_plural = 'Historias Clínicas'


class Partner(models.Model):
    """
    Partner information for patients in couples treatment
    """
    
    GENDER_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
    ]
    
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE, related_name='partner')
    
    first_name = models.CharField(max_length=100, verbose_name='Nombre')
    last_name = models.CharField(max_length=100, verbose_name='Apellido')
    date_of_birth = models.DateField(verbose_name='Fecha de Nacimiento')
    biological_sex = models.CharField(max_length=1, choices=GENDER_CHOICES)
    dni = models.CharField(max_length=20, verbose_name='DNI')
    
    # Genital background
    genital_background = models.TextField(blank=True, verbose_name='Antecedentes Genitales')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - Pareja de {self.patient}"
    
    class Meta:
        verbose_name = 'Pareja'
        verbose_name_plural = 'Parejas'
