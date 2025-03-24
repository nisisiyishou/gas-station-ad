from rest_framework import serializers
from .models import GasStation

class GasStationSerializer(serializers.ModelSerializer):
    latitude = serializers.FloatField(source='location.y', read_only=True)
    longitude = serializers.FloatField(source='location.x', read_only=True)
    board_count = serializers.SerializerMethodField()
    
    class Meta:
        model = GasStation
        fields = [
            'id', 'name', 'address', 'brand', 'latitude', 'longitude', 
            'is_active', 'board_count', 'created_at'
        ]
    
    def get_board_count(self, obj):
        return obj.boards.filter(is_available=True).count()