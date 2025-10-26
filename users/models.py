from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom user model with role-based access control.
    Roles: ADMIN, MEDICAL_DIRECTOR, DOCTOR, LAB_OPERATOR, PATIENT
    """
    
    ROLE_CHOICES = [
        ('ADMIN', 'Administrador'),
        ('MEDICAL_DIRECTOR', 'Director Médico'),
        ('DOCTOR', 'Médico'),
        ('LAB_OPERATOR', 'Operador de Laboratorio'),
        ('PATIENT', 'Paciente'),
    ]

    GENDER_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
    ]
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='PATIENT')
    phone = models.CharField(max_length=20, blank=True, verbose_name='Teléfono')
    dni = models.CharField(max_length=20, unique=True, null=True, blank=True, verbose_name='DNI')
    biological_sex = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True, verbose_name='Sexo Biológico')
    date_of_birth = models.DateField(null=True, blank=True, verbose_name='Fecha de Nacimiento')
    
    def is_admin(self):
        return self.role == 'ADMIN'
    
    def is_medical_director(self):
        return self.role == 'MEDICAL_DIRECTOR'
    
    def is_doctor(self):
        return self.role in ['DOCTOR', 'MEDICAL_DIRECTOR']
    
    def is_lab_operator(self):
        return self.role in ['LAB_OPERATOR', 'MEDICAL_DIRECTOR']
    
    def is_patient(self):
        return self.role == 'PATIENT'
    
    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
