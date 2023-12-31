import time
from rest_framework.response import Response
from rest_framework import generics, permissions

from . import models
from . import serializers

# Create your views here.


class ProjectListAPIView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny,]
    queryset = models.Project.objects.all()
    serializer_class = serializers.ProjectSerializer
    lookup_field = 'id'
    ordering = ['sequence_number', '-create_at']

    def list(self, request):
        queryset = self.filter_queryset(
            self.get_queryset()).order_by('sequence_number')
        serializer = self.get_serializer(queryset, many=True)
        serializer_data = serializer.data
        for data in serializer_data:
            instance = self.queryset.get(pk=data['id'])
            images = instance.images.all().filter(status=True).order_by('-id')
            data['images'] = serializers.ImageSerializer(
                images, many=True).data
        return Response(serializer_data)


class ProjectDetailAPIView(generics.RetrieveAPIView):
    permission_classes = [permissions.AllowAny,]
    queryset = models.Project.objects.all()
    serializer_class = serializers.ProjectSerializer

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        images = instance.images.all().filter(status=True).order_by('-id')
        comments = instance.comments.all().filter(status=True).order_by('-create_at')
        serializer = self.get_serializer(instance=instance)
        serializer_data = serializer.data
        serializer_data['images'] = serializers.ImageSerializer(
            images, many=True).data
        serializer_data['comments'] = serializers.CommentSerializer(
            comments, many=True).data
        return Response(serializer_data)


class CommentCreateAPIView(generics.CreateAPIView):
    queryset = models.Comment.objects.all()
    serializer_class = serializers.CommentSerializer


class MyLinkListAPIView(generics.ListAPIView):
    queryset = models.MyLink.objects.filter(is_private=False).all()
    serializer_class = serializers.MyLinkSerializer


class MyLinkDetailAPIView(generics.RetrieveAPIView):
    queryset = models.MyLink.objects.filter(is_private=False).all()
    serializer_class = serializers.MyLinkSerializer
