from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import CommercialBoard, Advertisement
from .serializers import CommercialBoardSerializer, AdvertisementSerializer
from stations.models import GasStation

class CommercialBoardViewSet(viewsets.ModelViewSet):
    queryset = CommercialBoard.objects.filter(is_available=True)
    serializer_class = CommercialBoardSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    @action(detail=False, methods=['get'])
    def by_station(self, request):
        """Get boards for a specific gas station"""
        station_id = request.query_params.get('station_id')
        if not station_id:
            return Response({"error": "station_id is required"}, status=400)
        
        boards = self.queryset.filter(gas_station_id=station_id)
        serializer = self.get_serializer(boards, many=True)
        return Response(serializer.data)

class AdvertisementViewSet(viewsets.ModelViewSet):
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        # Calculate total price based on duration and board price
        board = get_object_or_404(CommercialBoard, id=self.request.data.get('board'))
        start_date = serializer.validated_data.get('start_date')
        end_date = serializer.validated_data.get('end_date')
        days = (end_date - start_date).days + 1  # inclusive
        total_price = board.price_per_day * days
        
        serializer.save(total_price=total_price)