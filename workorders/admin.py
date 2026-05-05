from django.contrib import admin
from .models import WorkOrder, WorkReport


@admin.register(WorkOrder)
class WorkOrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'equipment', 'order_type', 'priority', 'status', 'assigned_user', 'created_at']
    list_filter = ['status', 'order_type', 'priority']
    search_fields = ['equipment__inv_number', 'description']
    ordering = ['-created_at']
    raw_id_fields = ['equipment', 'assigned_user', 'created_by']


@admin.register(WorkReport)
class WorkReportAdmin(admin.ModelAdmin):
    list_display = ['id', 'work_order', 'report_date', 'hours_spent', 'technician_signature']
    list_filter = ['report_date']
    search_fields = ['work_order__equipment__inv_number']
