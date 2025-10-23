# Sistema de Clínica de Fertilidad

Sistema de gestión para clínica de fertilidad desarrollado con Django.

## Características

- **Gestión de Usuarios**: 5 roles (Admin, Director Médico, Médico, Operador de Laboratorio, Paciente)
- **Gestión de Pacientes**: Registro, historias clínicas, información de parejas
- **Tratamientos**: Inicio de tratamientos, protocolos de estimulación, monitoreo
- **Laboratorio**: Gestión de punciones, óvulos, embriones, transferencias
- **Órdenes Médicas**: Generación de órdenes de estudios y recetas
- **Productos Biológicos**: Seguimiento de óvulos y embriones criopreservados

## Instalación

1. **Clonar el repositorio**
\`\`\`bash
git clone <repository-url>
cd fertility-clinic-django
\`\`\`

2. **Crear entorno virtual**
\`\`\`bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
\`\`\`

3. **Instalar dependencias**
\`\`\`bash
pip install -r requirements.txt
\`\`\`

4. **Configurar variables de entorno**
\`\`\`bash
cp .env.example .env
# Editar .env con tus configuraciones
\`\`\`

5. **Ejecutar migraciones**
\`\`\`bash
python manage.py makemigrations
python manage.py migrate
\`\`\`

6. **Poblar base de datos con datos de prueba**
\`\`\`bash
python seed_database.py
\`\`\`

7. **Ejecutar servidor de desarrollo**
\`\`\`bash
python manage.py runserver
\`\`\`

## Usuarios de Prueba

Después de ejecutar `seed_data`, tendrás los siguientes usuarios:

- **Admin**: `admin` / `admin123`
- **Director Médico**: `director` / `director123`
- **Médicos**: `drlopez`, `dramartin` / `doctor123`
- **Operadores de Lab**: `labop1`, `labop2` / `labop123`
- **Pacientes**: `paciente1`, `paciente2`, `paciente3` / `paciente123`

## Estructura del Proyecto

\`\`\`
fertility_clinic/
├── core/                 # App principal (dashboard, vistas comunes)
├── users/                # Gestión de usuarios y autenticación
├── patients/             # Gestión de pacientes e historias clínicas
├── treatments/           # Gestión de tratamientos y órdenes médicas
├── laboratory/           # Gestión de laboratorio (óvulos, embriones)
├── templates/            # Templates HTML
├── static/               # Archivos estáticos (CSS, JS, imágenes)
└── media/                # Archivos subidos por usuarios
\`\`\`

## Módulos Externos (APIs)

Los siguientes módulos serán manejados por APIs externas:
- Turnos
- Laboratorio Genético
- Banco de Donaciones
- Pagos
- Avisos
- Calendario
- Órdenes
- Términos Médicos

## Tecnologías

- Django 5.0
- Django REST Framework
- SQLite (desarrollo)
- Bootstrap 4 (via Crispy Forms)
- Python 3.10+

## Licencia

Proyecto académico - Taller de Producción de Software
