from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile, AdPreview

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        extra_kwargs = {'password': {'write_only': True}}

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'company_name', 'phone', 'address']

class AdPreviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = AdPreview
        fields = [
            'id', 'user', 'board', 'media_file', 'adjusted_file',
            'created_at', 'converted_to_ad', 'advertisement'
        ]