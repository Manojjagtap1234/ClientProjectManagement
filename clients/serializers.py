from rest_framework import serializers
from .models import Client, Project
from django.contrib.auth.models import User

class ProjectSerializer(serializers.ModelSerializer):
    users = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True)

    class Meta:
        model = Project
        fields = ['id', 'project_name', 'users', 'created_at']

class ClientSerializer(serializers.ModelSerializer):
    projects = ProjectSerializer(many=True, read_only=True)

    class Meta:
        model = Client
        fields = ['id', 'client_name', 'projects', 'created_at', 'updated_at', 'created_by']

    def to_representation(self, instance):
        # Check if the view is a list view by looking at the request path
        if 'clients/' in self.context['request'].path:
            representation = super().to_representation(instance)
            representation.pop('projects')  # Remove 'projects' for the list view
            return representation
        return super().to_representation(instance)
