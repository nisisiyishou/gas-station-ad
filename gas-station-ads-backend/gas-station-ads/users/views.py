from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import UserProfile, AdPreview
from .serializers import UserSerializer, UserProfileSerializer, AdPreviewSerializer
import os
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """Get current user info"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Regular users can only see their own profile
        if not self.request.user.is_staff:
            return self.queryset.filter(user=self.request.user)
        return self.queryset

class AdPreviewViewSet(viewsets.ModelViewSet):
    queryset = AdPreview.objects.all()
    serializer_class = AdPreviewSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Users can only see their own previews
        if not self.request.user.is_staff:
            return self.queryset.filter(user=self.request.user)
        return self.queryset
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def adjust_media(self, request, pk=None):
        """Adjust preview media to fit the board dimensions"""
        preview = self.get_object()
        board = preview.board
        
        # Simple resize example - in production you'd want more sophisticated handling
        try:
            img = Image.open(preview.media_file)
            target_width = float(board.width)
            target_height = float(board.height)
            
            # Calculate aspect ratios
            img_aspect = img.width / img.height
            target_aspect = target_width / target_height
            
            if img_aspect > target_aspect:
                # Image is wider than target
                new_height = int(img.width / target_aspect)
                top = (img.height - new_height) // 2
                img = img.crop((0, top, img.width, top + new_height))
            else:
                # Image is taller than target
                new_width = int(img.height * target_aspect)
                left = (img.width - new_width) // 2
                img = img.crop((left, 0, left + new_width, img.height))
            
            # Resize to target dimensions
            img = img.resize((int(target_width), int(target_height)), Image.LANCZOS)
            
            # Save the adjusted image
            buffer = BytesIO()
            img.save(buffer, format=os.path.splitext(preview.media_file.name)[1][1:].upper())
            buffer.seek(0)
            
            filename = os.path.basename(preview.media_file.name)
            preview.adjusted_file.save(f"adjusted_{filename}", ContentFile(buffer.read()), save=True)
            
            serializer = self.get_serializer(preview)
            return Response(serializer.data)
            
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)