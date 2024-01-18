from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Room, Topic
from .forms import RoomForm

def login_portal(request):
    # if user is already logged in and tries to route the `/login`, the user will be redirected to the hompage.
    if request.user.is_authenticated:
        return redirect('homepage')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Username Doesn\'t Exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('homepage')
        else:
            messages.error(request, "Username or Password does not exist.")

    context = {}
    return render(request, 'api/login_register.html', context)

def logout_user(request):
    logout(request)
    return redirect('homepage')

def home(request):
    q = request.GET.get('q') if request.GET.get('q')!=None else ''

    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
        )
    topics = Topic.objects.all()
    room_count = rooms.count()

    context = {'rooms': rooms, 'topics': topics, 'room_count': room_count}
    return render(request, 'api/home.html', context)

@login_required(login_url='/login')
def room(request, pk):
    room = Room.objects.get(id=pk)    
    context = {'room': room}
    return render(request, 'api/room.html', context)

@login_required(login_url='/login')
def create_room(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('homepage')

    context = {'form': form}
    return render(request, 'api/room_form.html', context)

@login_required(login_url='/login')
def update_room(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse('You are not allowed to update this Room!!')

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('homepage')
        
    context = {'form': form}
    return render(request, 'api/room_form.html', context)

@login_required(login_url='/login')
def delete_room(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse('You are not allowed to delete this Room!!')
    
    if request.method == 'POST':
        room.delete()
        return redirect('homepage')
    return render(request, 'api/delete.html', {'obj': room})