from django.shortcuts import render
from .models import Room

# rooms = [
#     {
#         'id': 1,
#         'name': 'Let\'s Test out Comms-ee'
#     },
#     {
#         'id': 2,
#         'name': 'Building the server with Python-Django'
#     },
#     {
#         'id': 3,
#         'name': 'Using HTML Templating now, gonna change to React later'
#     }
# ]

def home(request):
    rooms = Room.objects.all()
    context = {'rooms': rooms}
    return render(request, 'api/home.html', context)

def room(request, pk):
    room = Room.objects.get(id=pk)    
    context = {'room': room}
    return render(request, 'api/room.html', context)