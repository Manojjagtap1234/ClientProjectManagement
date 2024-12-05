from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from .models import Client, Project
from .serializers import ClientSerializer, ProjectSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Client, Project, User
from rest_framework import status
from rest_framework import serializers





#Blank Request
def blank_request_view(request):
    return HttpResponse("<h1>This is the Clients Projects Manager</h1>")

# List/Create Clients
class ClientListCreateView(generics.ListCreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


# Retrieve/Update/Delete a Client
class ClientDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'


# Create a new Project for a Client
class ProjectCreateView(generics.CreateAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Get client by ID from URL parameter
        client_id = self.kwargs.get('client_id')
        client = get_object_or_404(Client, id=client_id)

        # Extract user IDs from the request body
        user_ids = self.request.data.get('users', [])
        if not user_ids:
            raise serializers.ValidationError({"error": "User IDs are required to assign users to the project."})

        # Filter and validate user IDs
        valid_users = User.objects.filter(id__in=user_ids)
        if len(valid_users) != len(user_ids):
            raise serializers.ValidationError({"error": "Some provided user IDs are invalid."})

        # Save the project with the selected users and the associated client
        project = serializer.save(client=client)
        project.users.set(valid_users)
        project.save()



# List all Projects assigned to the logged-in User
class UserProjectsListView(generics.ListAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Project.objects.all()
        return Project.objects.filter(users=self.request.user)

    

