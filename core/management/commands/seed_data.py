"""
Script to seed the database with test data
Run with: python manage.py seed_data
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from patients.models import Patient, MedicalHistory, Partner
from treatments.models import Treatment, MonitoringDay, MedicalOrder
from laboratory.models import Puncture, Oocyte, Embryo
from datetime import datetime, timedelta
import random

User = get_user_model()


class Command(BaseCommand):
    help = 'Seed the database with test data'

    def handle(self, *args, **kwargs):
        self.stdout.write('🌱 Seeding database...\n')
        
        # Create admin user
        admin, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@fertilidad.com',
                'first_name': 'Admin',
                'last_name': 'Sistema',
                'role': 'ADMIN',
                'dni': '20123456',
                'biological_sex': 'M',
                'date_of_birth': '1980-01-01',
                'phone': '11-5555-0000',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        if created:
            admin.set_password('admin123')
            admin.save()
            self.stdout.write('✓ Admin creado: admin / admin123')
        
        # Create medical director
        director, created = User.objects.get_or_create(
            username='director',
            defaults={
                'email': 'director@fertilidad.com',
                'first_name': 'María',
                'last_name': 'González',
                'role': 'MEDICAL_DIRECTOR',
                'dni': '25234567',
                'biological_sex': 'F',
                'date_of_birth': '1975-03-15',
                'phone': '11-5555-0001',
            }
        )
        if created:
            director.set_password('director123')
            director.save()
            self.stdout.write('✓ Director Médico creado: director / director123')
        
        # Create doctors
        doctors = []
        doctor_data = [
            ('drlopez', 'Carlos', 'López', 'carlos.lopez@fertilidad.com', '11-5555-0002', '28345678', 'M', '1982-07-20'),
            ('dramartin', 'Laura', 'Martín', 'laura.martin@fertilidad.com', '11-5555-0003', '30456789', 'F', '1985-11-10'),
        ]
        
        for username, first_name, last_name, email, phone, dni, sex, dob in doctor_data:
            doctor, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': email,
                    'first_name': first_name,
                    'last_name': last_name,
                    'role': 'DOCTOR',
                    'phone': phone,
                    'dni': dni,
                    'biological_sex': sex,
                    'date_of_birth': dob,
                }
            )
            if created:
                doctor.set_password('doctor123')
                doctor.save()
                self.stdout.write(f'✓ Médico creado: {username} / doctor123')
            doctors.append(doctor)
        
        # Create lab operators
        operators = []
        operator_data = [
            ('labop1', 'Ana', 'Rodríguez', 'ana.rodriguez@fertilidad.com', '11-5555-0004', '32567890', 'F', '1988-05-25'),
            ('labop2', 'Pedro', 'Fernández', 'pedro.fernandez@fertilidad.com', '11-5555-0005', '33678901', 'M', '1990-09-12'),
        ]
        
        for username, first_name, last_name, email, phone, dni, sex, dob in operator_data:
            operator, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': email,
                    'first_name': first_name,
                    'last_name': last_name,
                    'role': 'LAB_OPERATOR',
                    'phone': phone,
                    'dni': dni,
                    'biological_sex': sex,
                    'date_of_birth': dob,
                }
            )
            if created:
                operator.set_password('labop123')
                operator.save()
                self.stdout.write(f'✓ Operador de Lab creado: {username} / labop123')
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
                    'dni': dni,
                    'biological_sex': sex,
                    'date_of_birth': dob,
                }
            )
            if created:
                user.set_password('paciente123')
                user.save()
                self.stdout.write(f'✓ Paciente creado: {username} / paciente123')
            
            patient, created = Patient.objects.get_or_create(
                user=user,
                defaults={
                    'occupation': 'Empleada',
                    'medical_coverage': 'OSDE',
                    'member_number': f'OSDE-{dni}',
                }
            )
            patients.append((patient, first_name, last_name))
        
        # Create medical histories and treatments
        for i, (patient, first_name, last_name) in enumerate(patients):
            # Create medical history
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
            
            # Create treatment
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
                # Create monitoring days
                for j in range(3):
                    MonitoringDay.objects.create(
                        treatment=treatment,
                        date=datetime.now().date() + timedelta(days=j+5),
                        notes=f'Monitoreo día {j+1}',
                        completed=False,
                    )
                
                # Create medical orders
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
                
                # Create puncture for first patient only (as example)
                if i == 0:
                    operator = random.choice(operators)
                    puncture = Puncture.objects.create(
                        treatment=treatment,
                        operator=operator,
                        date=datetime.now() - timedelta(days=2),
                        operating_room='Quirófano 1',
                        complications='Sin complicaciones',
                    )
                    
                    # Create oocytes
                    for k in range(8):
                        state = random.choice(['MATURE', 'MATURE', 'MATURE', 'IMMATURE', 'VERY_IMMATURE'])
                        oocyte = Oocyte.objects.create(
                            puncture=puncture,
                            oocyte_id=f'OVO_{datetime.now().strftime("%Y%m%d")}_{last_name.upper()}_{first_name.upper()}_{k+1:02d}',
                            initial_state=state,
                            current_state=state,
                        )
                        
                        # Create embryo for some mature oocytes
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
        
        self.stdout.write('\n✅ Base de datos poblada exitosamente!')
        self.stdout.write('\n📋 Usuarios de prueba:')
        self.stdout.write('  Admin: admin / admin123')
        self.stdout.write('  Director: director / director123')
        self.stdout.write('  Médicos: drlopez, dramartin / doctor123')
        self.stdout.write('  Lab Ops: labop1, labop2 / labop123')
        self.stdout.write('  Pacientes: paciente1, paciente2, paciente3 / paciente123')
