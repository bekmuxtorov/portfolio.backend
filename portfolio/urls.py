from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # for projects section
    path('projects/', views.ProjectListAPIView.as_view()),
    path('projects/<int:pk>/', views.ProjectDetailAPIView.as_view()),

    # for comment section
    path('comments/create/', views.CommentCreateAPIView.as_view()),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
