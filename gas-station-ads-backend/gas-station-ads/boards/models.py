# boards/models.py
from django.db import models
from stations.models import GasStation

class CommercialBoard(models.Model):
    LOCATION_CHOICES = [
        ('entrance', 'Entrance'),
        ('checkout', 'Checkout Area'),
        ('pump', 'Fuel Pump'),
        ('exterior', 'Exterior Wall'),
        ('interior', 'Interior Wall'),
    ]
    
    TYPE_CHOICES = [
        ('digital', 'Digital Screen'),
        ('poster', 'Poster'),
        ('billboard', 'Billboard'),
    ]
    
    gas_station = models.ForeignKey(GasStation, on_delete=models.CASCADE, related_name='boards')
    board_id = models.CharField(max_length=20, unique=True)  # Custom ID for the board
    board_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    location_in_station = models.CharField(max_length=20, choices=LOCATION_CHOICES)
    width = models.DecimalField(max_digits=6, decimal_places=2, help_text="Width in cm")
    height = models.DecimalField(max_digits=6, decimal_places=2, help_text="Height in cm")
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    is_available = models.BooleanField(default=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='board_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.board_id} at {self.gas_station.name}"

class Advertisement(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    board = models.ForeignKey(CommercialBoard, on_delete=models.CASCADE, related_name='advertisements')
    customer_name = models.CharField(max_length=100)
    customer_email = models.EmailField()
    original_media = models.FileField(upload_to='ad_originals/')
    adjusted_media = models.FileField(upload_to='ad_adjusted/', blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.customer_name}'s ad on {self.board.board_id}"