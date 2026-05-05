from django.contrib import admin
from .models import Equipment, MaintenanceSchedule


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ['inv_number', 'name', 'type', 'workshop', 'status', 'install_date', 'last_maintenance']
    list_filter = ['status', 'type', 'workshop']
    search_fields = ['inv_number', 'name']
    ordering = ['inv_number']


@admin.register(MaintenanceSchedule)
class MaintenanceScheduleAdmin(admin.ModelAdmin):
    list_display = ['equipment', 'frequency_days', 'next_due', 'last_completed', 'is_active']
    list_filter = ['is_active']
    search_fields = ['equipment__inv_number']
