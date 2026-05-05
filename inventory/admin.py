from django.contrib import admin
from .models import SparePart, PartRequest


@admin.register(SparePart)
class SparePartAdmin(admin.ModelAdmin):
    list_display = ['sku', 'name', 'category', 'unit_price', 'current_stock', 'min_stock', 'warehouse_location', 'is_low_stock']
    list_filter = ['category', 'warehouse_location']
    search_fields = ['sku', 'name']
    ordering = ['sku']


@admin.register(PartRequest)
class PartRequestAdmin(admin.ModelAdmin):
    list_display = ['id', 'work_order', 'spare_part', 'quantity', 'status', 'requested_by', 'fulfilled_by']
    list_filter = ['status']
    search_fields = ['work_order__equipment__inv_number', 'spare_part__sku']
    ordering = ['-id']
