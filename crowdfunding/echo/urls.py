from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('echo/', views.ProjectList.as_view()),
    path('echo/<int:pk>', views.ProjectDetail.as_view()),
    path('pledge/', views.PledgeList.as_view()),
    path('pledge/<int:pk>', views.PledgeDetail.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)