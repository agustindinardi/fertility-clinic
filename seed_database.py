"""
Script to seed the database with test data
Run with: python seed_database.py
"""
import os
import sys
import django
from pathlib import Path
from datetime import datetime, timedelta
import random

# Add project root to Python path
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

# Setup Django - ajusta el nombre según tu proyecto
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fertility_clinic.settings')
django.setup()

from django.contrib.auth import get_user_model
from patients.models import Patient, MedicalHistory
from treatments.models import Treatment, MonitoringDay, MedicalOrder
from laboratory.models import Puncture, Oocyte, Embryo

User = get_user_model()


def seed_database():
    print('🌱 Seeding database...\n')
    
    # Create admin user
    admin, created = User.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@fertilidad.com',
            'first_name': 'Admin',
            'last_name': 'Sistema',
            'role': 'ADMIN',
            'is_staff': True,
            'is_superuser': True,
        }
    )
    if created:
        admin.set_password('admin123')
        admin.save()
        print('✓ Admin creado: admin / admin123')
    
    # Create medical director
    director, created = User.objects.get_or_create(
        username='director',
        defaults={
            'email': 'director@fertilidad.com',
            'first_name': 'María',
            'last_name': 'González',
            'role': 'MEDICAL_DIRECTOR',
            'phone': '11-5555-0001',
        }
    )
    if created:
        director.set_password('director123')
        director.save()
        print('✓ Director Médico creado: director / director123')
    
    # Create doctors
    doctors = []
    doctor_data = [
        ('drlopez', 'Carlos', 'López', 'carlos.lopez@fertilidad.com', '11-5555-0002'),
        ('dramartin', 'Laura', 'Martín', 'laura.martin@fertilidad.com', '11-5555-0003'),
    ]
    
    for username, first_name, last_name, email, phone in doctor_data:
        doctor, created = User.objects.get_or_create(
            username=username,
            defaults={
                'email': email,
                'first_name': first_name,
                'last_name': last_name,
                'role': 'DOCTOR',
                'phone': phone,
            }
        )
        if created:
            doctor.set_password('doctor123')
            doctor.save()
            print(f'✓ Médico creado: {username} / doctor123')
        doctors.append(doctor)
    
    # Create lab operators
    operators = []
    operator_data = [
        ('labop1', 'Ana', 'Rodríguez', 'ana.rodriguez@fertilidad.com', '11-5555-0004'),
        ('labop2', 'Pedro', 'Fernández', 'pedro.fernandez@fertilidad.com', '11-5555-0005'),
    ]
    
    for username, first_name, last_name, email, phone in operator_data:
        operator, created = User.objects.get_or_create(
            username=username,
            defaults={
                'email': email,
                'first_name': first_name,
                'last_name': last_name,
                'role': 'LAB_OPERATOR',
                'phone': phone,
            }
        )
        if created:
            operator.set_password('labop123')
            operator.save()
            print(f'✓ Operador de Lab creado: {username} / labop123')
        operators.append(operator)
    
    # Create patients
    patient_data = [
        ('paciente1', 'Sofía', 'Ramírez', 'sofia.ramirez@email.com', '11-6666-0001', '35123456', 'F', '1990-05-15'),
        ('paciente2', 'Lucía', 'Torres', 'lucia.torres@email.com', '11-6666-0002', '36234567', 'F', '1988-08-22'),
        ('paciente3', 'Valentina', 'Morales', 'valentina.morales@email.com', '11-6666-0003', '37345678', 'F', '1992-03-10'),
    ]
    
    patients = []
    for username, first_name, last_name, email, phone, dni, sex, dob in patient_data:
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                'email': email,
                'first_name': first_name,
                'last_name': last_name,
                'role': 'PATIENT',
                'phone': phone,
            }
        )
        if created:
            user.set_password('paciente123')
            user.save()
            print(f'✓ Paciente creado: {username} / paciente123')
        
        patient, created = Patient.objects.get_or_create(
            user=user,
            defaults={
                'dni': dni,
                'biological_sex': sex,
                'date_of_birth': dob,
                'occupation': 'Empleada',
                'medical_coverage': 'OSDE',
                'member_number': f'OSDE-{dni}',
            }
        )
        patients.append((patient, first_name, last_name))
    
    # Create medical histories and treatments
    for i, (patient, first_name, last_name) in enumerate(patients):
        history, created = MedicalHistory.objects.get_or_create(
            patient=patient,
            defaults={
                'clinical_background': 'Sin antecedentes clínicos relevantes',
                'surgical_background': 'Apendicectomía en 2010',
                'personal_background': 'No fumadora, actividad física regular',
                'family_background': 'Madre con diabetes tipo 2',
                'gynecological_background': 'Ciclos regulares, menarquia a los 12 años',
                'physical_exam': 'Peso: 65kg, Altura: 165cm, IMC: 23.9',
                'phenotype': 'Caucásico, cabello castaño, ojos marrones',
            }
        )
        
        doctor = random.choice(doctors)
        treatment, created = Treatment.objects.get_or_create(
            patient=patient,
            doctor=doctor,
            defaults={
                'objective': random.choice(['PREGNANCY', 'OOCYTE_PRESERVATION']),
                'status': 'ACTIVE',
                'stimulation_protocol': 'Protocolo antagonista con FSH recombinante',
                'medication_type': 'Gonal-F 300 UI',
                'medication_dose': '150 UI/día',
                'medication_duration': '10-12 días',
                'oocytes_viable': True,
                'sperm_viable': True,
            }
        )
        
        if created:
            for j in range(3):
                MonitoringDay.objects.create(
                    treatment=treatment,
                    date=datetime.now().date() + timedelta(days=j+5),
                    notes=f'Monitoreo día {j+1}',
                    completed=False,
                )
            
            MedicalOrder.objects.create(
                treatment=treatment,
                order_type='STUDY',
                description='Estudios hormonales: FSH, LH, Estradiol, Progesterona, AMH',
            )
            
            MedicalOrder.objects.create(
                treatment=treatment,
                order_type='PRESCRIPTION',
                description='Gonal-F 300 UI - Aplicar 150 UI subcutánea diaria por 10 días',
            )
            
            if i == 0:
                operator = random.choice(operators)
                puncture = Puncture.objects.create(
                    treatment=treatment,
                    operator=operator,
                    date=datetime.now() - timedelta(days=2),
                    operating_room='Quirófano 1',
                    complications='Sin complicaciones',
                )
                
                for k in range(8):
                    state = random.choice(['MATURE', 'MATURE', 'MATURE', 'IMMATURE', 'VERY_IMMATURE'])
                    oocyte = Oocyte.objects.create(
                        puncture=puncture,
                        oocyte_id=f'OVO_{datetime.now().strftime("%Y%m%d")}_{last_name.upper()}_{first_name.upper()}_{k+1:02d}',
                        initial_state=state,
                        current_state=state,
                    )
                    
                    if state == 'MATURE' and k < 4:
                        embryo = Embryo.objects.create(
                            oocyte=oocyte,
                            embryo_id=f'EMB_{datetime.now().strftime("%Y%m%d")}_{last_name.upper()}_{first_name.upper()}_{k+1:02d}',
                            fertilization_technique=random.choice(['IVF', 'ICSI']),
                            sperm_source='PARTNER',
                            quality=random.randint(3, 5),
                            current_state=random.choice(['DEVELOPING', 'CRYOPRESERVED']),
                        )
                        
                        if embryo.current_state == 'CRYOPRESERVED':
                            embryo.nitrogen_tube = f'N2-{random.randint(1, 20):03d}'
                            embryo.rack_number = f'R{random.randint(1, 10)}'
                            embryo.save()
    
    print('\n✅ Base de datos poblada exitosamente!')
    print('\n📋 Usuarios de prueba:')
    print('  Admin: admin / admin123')
    print('  Director: director / director123')
    print('  Médicos: drlopez, dramartin / doctor123')
    print('  Lab Ops: labop1, labop2 / labop123')
    print('  Pacientes: paciente1, paciente2, paciente3 / paciente123')


if __name__ == '__main__':
    try:
        seed_database()
    except Exception as e:
        print(f'\n❌ Error: {e}')
        import traceback
        traceback.print_exc()
        sys.exit(1)