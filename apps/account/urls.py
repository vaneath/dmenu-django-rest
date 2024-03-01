from django.urls import path
from knox import views as knox_views

from .views import LoginView, RegisterUserAPI

urlpatterns = [
    path('register/', RegisterUserAPI.as_view()),
    path('login/', LoginView.as_view()),
    path(r'logout/', knox_views.LogoutView.as_view(), name='knox_logout'),
    path(r'logoutall/', knox_views.LogoutAllView.as_view(), name='knox_logoutall'),
]
