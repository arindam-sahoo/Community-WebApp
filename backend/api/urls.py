from django.urls import path
from .views import *

urlpatterns = [
    path('login/', login_portal, name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', register_portal, name='register'),
    path('', home, name='homepage'),
    path('room/<str:pk>', room, name='room'),
    path('create-room/', create_room, name='create-room'),
    path('update-room/<str:pk>/', update_room, name='update-room'),
    path('delete-room/<str:pk>/', delete_room, name='delete-room'),
    path('delete-message/<str:pk>/', delete_message, name='delete-message'),
]