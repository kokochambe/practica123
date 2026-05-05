from django.db import models
from django.conf import settings


class WorkOrder(models.Model):
    """Наряд-заказ на техническое обслуживание и ремонт"""
    
    ORDER_TYPE_CHOICES = [
        ('planned', 'Плановое ТО'),
        ('emergency', 'Аварийный ремонт'),
        ('modernization', 'Модернизация'),
        ('inspection', 'Инспекция'),
    ]
    
    STATUS_CHOICES = [
        ('new', 'Новый'),
        ('assigned', 'Назначен'),
        ('in_progress', 'В работе'),
        ('pending_parts', 'Ожидание запчастей'),
        ('completed', 'Выполнен'),
        ('rejected', 'Отклонен'),
    ]
    
    PRIORITY_CHOICES = [
        (1, 'Критический'),
        (2, 'Высокий'),
        (3, 'Средний'),
        (4, 'Низкий'),
        (5, 'Отложенный'),
    ]
    
    equipment = models.ForeignKey('equipment.Equipment', on_delete=models.CASCADE, related_name='work_orders', verbose_name='Оборудование')
    order_type = models.CharField(max_length=30, choices=ORDER_TYPE_CHOICES, verbose_name='Тип работ')
    priority = models.IntegerField(choices=PRIORITY_CHOICES, default=3, verbose_name='Приоритет')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name='Статус')
    assigned_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_work_orders', verbose_name='Исполнитель')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='created_work_orders', verbose_name='Создал')
    description = models.TextField(default='Техническое обслуживание / устранение неисправности', verbose_name='Описание')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    started_at = models.DateTimeField(null=True, blank=True, verbose_name='Начало работ')
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name='Завершение работ')
    
    class Meta:
        verbose_name = 'Наряд-заказ'
        verbose_name_plural = 'Наряды-заказы'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['assigned_user']),
        ]
    
    def __str__(self):
        return f"Наряд #{self.id} - {self.equipment.inv_number}"


class WorkReport(models.Model):
    """Отчёт о выполненных работах"""
    
    work_order = models.ForeignKey(WorkOrder, on_delete=models.CASCADE, related_name='reports', verbose_name='Наряд-заказ')
    report_date = models.DateField(verbose_name='Дата отчёта')
    hours_spent = models.DecimalField(max_digits=4, decimal_places=1, verbose_name='Затрачено часов')
    description = models.TextField(default='Работы выполнены по регламенту. Замечаний нет.', verbose_name='Описание работ')
    technician_signature = models.CharField(max_length=100, blank=True, null=True, verbose_name='Подпись исполнителя')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    
    class Meta:
        verbose_name = 'Отчёт о работах'
        verbose_name_plural = 'Отчёты о работах'
    
    def __str__(self):
        return f"Отчёт для наряда #{self.work_order.id}"
