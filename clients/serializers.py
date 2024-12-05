from rest_framework import serializers
from .models import Client, Project
from django.contrib.auth.models import User

class ProjectSerializer(serializers.ModelSerializer):
    users = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        many=True,
        required=True,
        error_messages={
            "required": "You must specify at least one user to assign to the project.",
            "does_not_exist": "One or more user IDs are invalid.",
        }
    )

    class Meta:
        model = Project
        fields = ['id', 'project_name', 'users', 'client', 'created_at']

    def validate_users(self, value):
        if not value:
            raise serializers.ValidationError("At least one user must be assigned to the project.")
        return value




class ClientSerializer(serializers.ModelSerializer):
    projects = ProjectSerializer(many=True, read_only=True)

    class Meta:
        model = Client
        fields = ['id', 'client_name', 'projects', 'created_at', 'updated_at', 'created_by']