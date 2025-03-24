from django.contrib import admin
from django.contrib.gis.admin import ModelAdmin as GeoModelAdmin
from django import forms
from .models import GasStation

@admin.register(GasStation)
class GasStationAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'brand', 'is_active')
    search_fields = ('name', 'address', 'brand')
    list_filter = ('is_active', 'brand')
    
    # Add custom fields for easier latitude/longitude input
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['latitude'] = forms.DecimalField(
            label='Latitude',
            max_digits=10,
            decimal_places=6,
            required=False,
            initial=obj.latitude if obj else None
        )
        form.base_fields['longitude'] = forms.DecimalField(
            label='Longitude',
            max_digits=10,
            decimal_places=6,
            required=False,
            initial=obj.longitude if obj else None
        )
        return form
    
    def save_model(self, request, obj, form, change):
        if form.cleaned_data.get('latitude') and form.cleaned_data.get('longitude'):
            obj._latitude = form.cleaned_data.get('latitude')
            obj._longitude = form.cleaned_data.get('longitude')
        super().save_model(request, obj, form, change)