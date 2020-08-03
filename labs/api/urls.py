
from django.urls import include, path
from . import views

urlpatterns = [
  path('persons', views.persons)
]