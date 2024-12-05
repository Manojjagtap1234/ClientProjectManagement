from django.urls import path
from .views import ClientListCreateView, ClientDetailView, ProjectCreateView, UserProjectsListView
from .views import blank_request_view
from . import views
urlpatterns = [
    path('', blank_request_view, name='blank-request'), 
    path('clients/', ClientListCreateView.as_view(), name='client-list-create'),
    path('clients/<int:pk>/', ClientDetailView.as_view(), name='client-detail'), 
    path('clients/<int:client_id>/projects/', views.ProjectCreateView.as_view(), name='project-create'),
    path('projects/', views.UserProjectsListView.as_view(), name='user-projects-list'),
]