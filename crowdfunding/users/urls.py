from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views
from .views import ChangePasswordView


urlpatterns = [
    path('users/', views.CustomUserList.as_view()),
    path('users/<int:pk>/', views.CustomUserDetail.as_view()),
    path('users/<int:pk>/change-password/', ChangePasswordView.as_view(), name='change-password'),
]

urlpatterns = format_suffix_patterns(urlpatterns)