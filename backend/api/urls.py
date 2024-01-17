from django.urls import path
from .views import home, room, create_room, update_room, delete_room, login_portal, logout_user

urlpatterns = [
    path('login/', login_portal, name='login'),
    path('logout/', logout_user, name='logout'),
    path('', home, name='homepage'),
    path('room/<str:pk>', room, name='room'),
    path('create-room/', create_room, name='create-room'),
    path('update-room/<str:pk>/', update_room, name='update-room'),
    path('delete-room/<str:pk>/', delete_room, name='delete-room'),
]