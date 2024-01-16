from django.contrib import admin
from django.urls import path, include
from .views import home, room

urlpatterns = [
    path('', home, name='homepage'),
    path('room/<str:pk>', room, name='room'),
]