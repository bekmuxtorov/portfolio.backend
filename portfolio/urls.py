from django.urls import path
from . import views


urlpatterns = [
    path('projects/', views.ProjectListAPIView.as_view()),
    path('projects/<int:pk>/', views.ProjectDetailAPIView.as_view()),
]
