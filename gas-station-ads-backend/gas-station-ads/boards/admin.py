# boards/admin.py
from django.contrib import admin
from .models import CommercialBoard, Advertisement

@admin.register(CommercialBoard)
class CommercialBoardAdmin(admin.ModelAdmin):
    list_display = ('board_id', 'gas_station', 'board_type', 'width', 'height', 'price_per_day', 'is_available')
    list_filter = ('board_type', 'is_available', 'gas_station')
    search_fields = ('board_id', 'gas_station__name', 'description')

@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'board', 'start_date', 'end_date', 'status')
    list_filter = ('status', 'start_date', 'end_date')
    search_fields = ('customer_name', 'customer_email', 'board__board_id')

