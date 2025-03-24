from rest_framework import serializers
from .models import CommercialBoard, Advertisement
from stations.serializers import GasStationSerializer

class CommercialBoardSerializer(serializers.ModelSerializer):
    gas_station_detail = GasStationSerializer(source='gas_station', read_only=True)
    
    class Meta:
        model = CommercialBoard
        fields = [
            'id', 'board_id', 'gas_station', 'gas_station_detail', 'board_type',
            'location_in_station', 'width', 'height', 'price_per_day',
            'is_available', 'description', 'image', 'created_at'
        ]

class AdvertisementSerializer(serializers.ModelSerializer):
    board_detail = CommercialBoardSerializer(source='board', read_only=True)
    
    class Meta:
        model = Advertisement
        fields = [
            'id', 'board', 'board_detail', 'customer_name', 'customer_email',
            'original_media', 'adjusted_media', 'start_date', 'end_date',
            'total_price', 'status', 'notes', 'created_at'
        ]