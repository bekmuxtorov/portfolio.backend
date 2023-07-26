from rest_framework import serializers
from . import models


class ProjectSerializer(serializers.ModelSerializer):
    images = serializers.ImageField()

    class Meta:
        model = models.Project
        fields = '__all__'


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Image
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Comment
        fields = ('project', 'full_name', 'text', 'date_difference')
