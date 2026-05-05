from django.db import models
from django.conf import settings


class Equipment(models.Model):
    """Реестр оборудования"""
    
    STATUS_CHOICES = [
        ('active', 'В эксплуатации'),
        ('maintenance', 'На обслуживании'),
        ('out_of_service', 'Неисправно'),
        ('decommissioned', 'Списано'),
    ]
    
    TYPE_CHOICES = [
        ('Насосы', 'Насосы'),
        ('Компрессоры', 'Компрессоры'),
        ('Электропривод', 'Электропривод'),
        ('Механика', 'Механика'),
        ('Вентиляция', 'Вентиляция'),
        ('Транспорт', 'Транспорт'),
        ('Металлообработка', 'Металлообработка'),
        ('Энергетика', 'Энергетика'),
        ('Электрика', 'Электрика'),
        ('Автоматика', 'Автоматика'),
    ]
    
    inv_number = models.CharField(max_length=30, unique=True, verbose_name='Инвентарный номер')
    name = models.CharField(max_length=200, verbose_name='Наименование')
    type = models.CharField(max_length=50, choices=TYPE_CHOICES, verbose_name='Тип оборудования')
    workshop = models.CharField(max_length=50, verbose_name='Цех/Участок')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active', verbose_name='Статус')
    install_date = models.DateField(null=True, blank=True, verbose_name='Дата установки')
    warranty_until = models.DateField(null=True, blank=True, verbose_name='Гарантия до')
    last_maintenance = models.DateField(null=True, blank=True, verbose_name='Последнее ТО')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    
    class Meta:
        verbose_name = 'Оборудование'
        verbose_name_plural = 'Оборудование'
        ordering = ['inv_number']
        indexes = [
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"{self.inv_number} - {self.name}"


class MaintenanceSchedule(models.Model):
    """График технического обслуживания"""
    
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, related_name='schedules', verbose_name='Оборудование')
    frequency_days = models.PositiveIntegerField(verbose_name='Периодичность (дней)')
    next_due = models.DateField(verbose_name='Следующее ТО')
    last_completed = models.DateField(null=True, blank=True, verbose_name='Последнее выполненное')
    checklist = models.TextField(default='Проверка масла, натяжение, очистка фильтров, смазка, замер вибрации', verbose_name='Чек-лист')
    is_active = models.BooleanField(default=True, verbose_name='Активен')
    
    class Meta:
        verbose_name = 'График ТО'
        verbose_name_plural = 'Графики ТО'
    
    def __str__(self):
        return f"График для {self.equipment.inv_number}"
