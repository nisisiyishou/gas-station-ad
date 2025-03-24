from django.db import models
from django.contrib.auth.models import User
from boards.models import Advertisement

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    
    def __str__(self):
        return self.user.username

class AdPreview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='previews')
    board = models.ForeignKey('boards.CommercialBoard', on_delete=models.CASCADE)
    media_file = models.FileField(upload_to='previews/')
    adjusted_file = models.FileField(upload_to='previews_adjusted/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    converted_to_ad = models.BooleanField(default=False)
    advertisement = models.ForeignKey(Advertisement, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.username}'s preview for {self.board.board_id}"