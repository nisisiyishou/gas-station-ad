from rest_framework import viewsets, permissions
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import GasStation
from .serializers import GasStationSerializer


class GasStationViewSet(viewsets.ModelViewSet):
    queryset = GasStation.objects.all()
    serializer_class = GasStationSerializer
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        
        # Debug info
        print(f"Number of stations in queryset: {queryset.count()}")
        for station in queryset:
            print(f"Station: {station.name}, boards: {station.boards.count()}")
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


@action(detail=False, methods=["get"])
def nearby(self, request):
    """Get gas stations near a specific location"""
    lat = request.query_params.get("lat")
    lng = request.query_params.get("lng")
    distance = request.query_params.get("distance", 5)  # default 5km

    if not lat or not lng:
        return Response({"error": "Latitude and longitude are required"}, status=400)

    try:
        point = Point(float(lng), float(lat))

        # Check if there are any stations in the database
        if GasStation.objects.count() == 0:
            return Response(
                {"stations": [], "message": "No gas stations available yet"}, status=200
            )

        stations = GasStation.objects.filter(
            location__distance_lte=(point, D(km=float(distance))), is_active=True
        ).order_by("location__distance", "name")

        serializer = self.get_serializer(stations, many=True)
        return Response(serializer.data)
    except Exception as e:
        # Log the error for debugging
        import logging

        logger = logging.getLogger(__name__)
        logger.error(f"Error in nearby stations: {str(e)}")

        # Return a user-friendly error
        return Response(
            {"error": "Could not process location data", "details": str(e)}, status=500
        )
