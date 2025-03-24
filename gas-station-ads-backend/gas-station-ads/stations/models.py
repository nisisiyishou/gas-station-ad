# stations/models.py
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point

class GasStation(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    location = models.PointField(geography=True)  # Geographic point (longitude, latitude)
    brand = models.CharField(max_length=50, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    @property
    def latitude(self):
        return self.location.y
    
    @property
    def longitude(self):
        return self.location.x
    
    def save(self, *args, **kwargs):
        # If location is provided as separate lat/long (useful for admin)
        if hasattr(self, '_latitude') and hasattr(self, '_longitude'):
            self.location = Point(float(self._longitude), float(self._latitude))
        super().save(*args, **kwargs)