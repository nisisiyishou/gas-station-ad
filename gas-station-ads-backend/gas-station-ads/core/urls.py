from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from stations.views import GasStationViewSet
from boards.views import CommercialBoardViewSet, AdvertisementViewSet
from users.views import UserViewSet, UserProfileViewSet, AdPreviewViewSet

# Create a router for the API
router = DefaultRouter()
router.register(r'stations', GasStationViewSet)
router.register(r'boards', CommercialBoardViewSet)
router.register(r'advertisements', AdvertisementViewSet)
router.register(r'users', UserViewSet)
router.register(r'profiles', UserProfileViewSet)
router.register(r'previews', AdPreviewViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)