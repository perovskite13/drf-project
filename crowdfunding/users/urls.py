from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views
from .views import ChangePasswordView, CreateAccountView,VerifyEmail



urlpatterns = [
    path('users/', views.CustomUserList.as_view()),
    path('users/<int:pk>/', views.CustomUserDetail.as_view()),
    path('users/<int:pk>/change-password/', ChangePasswordView.as_view(), name='change-password'),
    #path('create-account/', CreateAccountView.as_view(), name = 'createAccount'),
    path('email-verify/', VerifyEmail.as_view(), name = 'email-verify'),

]

urlpatterns = format_suffix_patterns(urlpatterns)