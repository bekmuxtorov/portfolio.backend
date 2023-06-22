from rest_framework import generics, permissions

from . import models
from . import serializers

# Create your views here.


class ProjectListAPIView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny,]
    queryset = models.Project.objects.all()
    serializer_class = serializers.ProjectSerializer


class ProjectDetailAPIView(generics.RetrieveAPIView):
    permission_classes = [permissions.AllowAny,]
    queryset = models.Project.objects.all()
    serializer_class = serializers.ProjectSerializer
