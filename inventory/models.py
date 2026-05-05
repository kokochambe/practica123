from django.db import models
from django.conf import settings


class SparePart(models.Model):
    """Справочник запчастей и материалов"""
    
    sku = models.CharField(max_length=30, unique=True, verbose_name='Артикул')
    name = models.CharField(max_length=200, verbose_name='Наименование')
    category = models.CharField(max_length=50, blank=True, null=True, verbose_name='Категория')
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Цена за ед.')
    min_stock = models.PositiveIntegerField(default=5, verbose_name='Мин. остаток')
    current_stock = models.PositiveIntegerField(default=0, verbose_name='Текущий остаток')
    warehouse_location = models.CharField(max_length=30, blank=True, null=True, verbose_name='Место на складе')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    
    class Meta:
        verbose_name = 'Запчасть'
        verbose_name_plural = 'Запчасти'
        ordering = ['sku']
    
    def __str__(self):
        return f"{self.sku} - {self.name}"
    
    @property
    def is_low_stock(self):
        return self.current_stock <= self.min_stock


class PartRequest(models.Model):
    """Заявка на выдачу запчастей"""
    
    STATUS_CHOICES = [
        ('requested', 'Запрошено'),
        ('approved', 'Утверждено'),
        ('issued', 'Выдано'),
        ('rejected', 'Отклонено'),
    ]
    
    work_order = models.ForeignKey('workorders.WorkOrder', on_delete=models.CASCADE, related_name='part_requests', verbose_name='Наряд-заказ')
    spare_part = models.ForeignKey(SparePart, on_delete=models.CASCADE, related_name='requests', verbose_name='Запчасть')
    quantity = models.PositiveIntegerField(verbose_name='Количество')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='requested', verbose_name='Статус')
    requested_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='requested_parts', verbose_name='Запросил')
    fulfilled_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='fulfilled_parts', verbose_name='Выдал')
    fulfilled_at = models.DateTimeField(null=True, blank=True, verbose_name='Дата выдачи')
    
    class Meta:
        verbose_name = 'Заявка на запчасти'
        verbose_name_plural = 'Заявки на запчасти'
        ordering = ['-id']
    
    def __str__(self):
        return f"Заявка #{self.id} для наряда #{self.work_order.id}"
