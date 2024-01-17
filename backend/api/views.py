from django.shortcuts import render, redirect
from .models import Room
from .forms import RoomForm

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

def create_room(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('homepage')

    context = {'form': form}
    return render(request, 'api/room_form.html', context)

def update_room(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('homepage')
        
    context = {'form': form}
    return render(request, 'api/room_form.html', context)

def delete_room(request, pk):
    room = Room.objects.get(id=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('homepage')
    return render(request, 'api/delete.html', {'obj': room})