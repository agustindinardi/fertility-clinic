from django.db import models
from django.conf import settings
from treatments.models import Treatment


class Puncture(models.Model):
    """
    Puncture procedure to extract oocytes
    """
    
    treatment = models.OneToOneField(Treatment, on_delete=models.CASCADE, related_name='puncture')
    operator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='punctures_performed')
    
    date = models.DateTimeField(verbose_name='Fecha y Hora')
    operating_room = models.CharField(max_length=50, verbose_name='Número de Quirófano')
    complications = models.TextField(blank=True, verbose_name='Complicaciones')
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Punción - {self.treatment.patient} - {self.date.date()}"
    
    class Meta:
        verbose_name = 'Punción'
        verbose_name_plural = 'Punciones'


class Oocyte(models.Model):
    """
    Oocyte extracted during puncture
    """
    
    STATE_CHOICES = [
        ('VERY_IMMATURE', 'Muy Inmaduro'),
        ('IMMATURE', 'Inmaduro'),
        ('MATURE', 'Maduro'),
        ('FERTILIZED', 'Fertilizado'),
        ('DISCARDED', 'Descartado'),
        ('CRYOPRESERVED', 'Criopreservado'),
    ]
    
    puncture = models.ForeignKey(Puncture, on_delete=models.CASCADE, related_name='oocytes')
    oocyte_id = models.CharField(max_length=100, unique=True, verbose_name='ID del Óvulo')
    
    initial_state = models.CharField(max_length=20, choices=STATE_CHOICES, verbose_name='Estado Inicial')
    current_state = models.CharField(max_length=20, choices=STATE_CHOICES, verbose_name='Estado Actual')
    
    maturation_time = models.IntegerField(null=True, blank=True, verbose_name='Tiempo de Maduración (horas)')
    discard_reason = models.TextField(blank=True, verbose_name='Motivo de Descarte')
    
    # Cryopreservation info
    nitrogen_tube = models.CharField(max_length=50, blank=True, verbose_name='Tubo de Nitrógeno')
    rack_number = models.CharField(max_length=50, blank=True, verbose_name='Número de Rack')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.oocyte_id} - {self.get_current_state_display()}"
    
    class Meta:
        verbose_name = 'Óvulo'
        verbose_name_plural = 'Óvulos'


class OocyteStateHistory(models.Model):
    """
    History of state changes for an oocyte
    """
    
    oocyte = models.ForeignKey(Oocyte, on_delete=models.CASCADE, related_name='state_history')
    from_state = models.CharField(max_length=20, verbose_name='Estado Anterior')
    to_state = models.CharField(max_length=20, verbose_name='Nuevo Estado')
    notes = models.TextField(blank=True, verbose_name='Notas')
    changed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Historial de Estado de Óvulo'
        verbose_name_plural = 'Historiales de Estado de Óvulos'
        ordering = ['-created_at']


class Embryo(models.Model):
    """
    Embryo resulting from fertilization
    """
    
    STATE_CHOICES = [
        ('DEVELOPING', 'En Desarrollo'),
        ('TRANSFERRED', 'Transferido'),
        ('CRYOPRESERVED', 'Criopreservado'),
        ('DISCARDED', 'Descartado'),
    ]
    
    FERTILIZATION_TECHNIQUE_CHOICES = [
        ('IVF', 'FIV - Fertilización In Vitro'),
        ('ICSI', 'ICSI - Inyección Intracitoplasmática'),
    ]
    
    SPERM_SOURCE_CHOICES = [
        ('PARTNER', 'Pareja'),
        ('DONOR', 'Donante'),
    ]
    
    oocyte = models.OneToOneField(Oocyte, on_delete=models.CASCADE, related_name='embryo')
    embryo_id = models.CharField(max_length=100, unique=True, verbose_name='ID del Embrión')
    
    fertilization_technique = models.CharField(max_length=10, choices=FERTILIZATION_TECHNIQUE_CHOICES, verbose_name='Técnica de Fertilización')
    sperm_source = models.CharField(max_length=10, choices=SPERM_SOURCE_CHOICES, verbose_name='Origen del Esperma')
    
    quality = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)], verbose_name='Calidad (1-5)')
    current_state = models.CharField(max_length=20, choices=STATE_CHOICES, default='DEVELOPING', verbose_name='Estado Actual')
    
    # PGT results
    pgt_performed = models.BooleanField(default=False, verbose_name='PGT Realizado')
    pgt_result = models.BooleanField(null=True, blank=True, verbose_name='Resultado PGT (OK/No OK)')
    
    # Cryopreservation info
    nitrogen_tube = models.CharField(max_length=50, blank=True, verbose_name='Tubo de Nitrógeno')
    rack_number = models.CharField(max_length=50, blank=True, verbose_name='Número de Rack')
    
    discard_reason = models.TextField(blank=True, verbose_name='Motivo de Descarte')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.embryo_id} - Calidad {self.quality} - {self.get_current_state_display()}"
    
    class Meta:
        verbose_name = 'Embrión'
        verbose_name_plural = 'Embriones'


class EmbryoTransfer(models.Model):
    """
    Embryo transfer procedure and results
    """
    
    embryo = models.OneToOneField(Embryo, on_delete=models.CASCADE, related_name='transfer')
    scheduled_date = models.DateField(verbose_name='Fecha Programada')
    performed_date = models.DateField(null=True, blank=True, verbose_name='Fecha Realizada')
    
    # Results
    beta_positive = models.BooleanField(null=True, blank=True, verbose_name='Beta Positiva')
    gestational_sac = models.BooleanField(null=True, blank=True, verbose_name='Saco Gestacional')
    clinical_pregnancy = models.BooleanField(null=True, blank=True, verbose_name='Embarazo Clínico')
    live_birth = models.BooleanField(null=True, blank=True, verbose_name='Nacido Vivo')
    
    notes = models.TextField(blank=True, verbose_name='Notas')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Transferencia - {self.embryo.embryo_id} - {self.scheduled_date}"
    
    class Meta:
        verbose_name = 'Transferencia de Embrión'
        verbose_name_plural = 'Transferencias de Embriones'
