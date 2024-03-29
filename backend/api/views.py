from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import Room, Topic, Message, User
from .forms import RoomForm, UserForm, MyUserCreationForm

def login_portal(request):
    page = 'login'

    # if user is already logged in and tries to route the `/login`, the user will be redirected to the hompage.
    if request.user.is_authenticated:
        return redirect('homepage')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
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

    context = {'page': page}
    return render(request, 'api/login_register.html', context)

def logout_user(request):
    logout(request)
    return redirect('homepage')

def register_portal(request):
    page = 'register'
    form = MyUserCreationForm()
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('homepage')
        else:
            messages.error(request, 'An error occured during registration!!')
    return render(request, 'api/login_register.html', {'form': form})

def home(request):
    q = request.GET.get('q') if request.GET.get('q')!=None else ''

    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
        )
    topics = Topic.objects.all()
    room_count = rooms.count()
    room_messages = Message.objects.filter(
        Q(room__name__icontains=q)
        )

    context = {'rooms': rooms, 'topics': topics, 'room_count': room_count, 'room_messages': room_messages}
    return render(request, 'api/home.html', context)

@login_required(login_url='/login')
def room(request, pk):
    room = Room.objects.get(id=pk)
    participants = room.participants.all()

    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('message_body')
        )
        # Once a user messages in the room, the user gets added as a roommate/participant
        room.participants.add(request.user)
        return redirect('room', pk=room.id)

    # Room Parent Class has the Message as it's Child Class. So we are fetching all the messages belonging to the room.
    room_messages = room.message_set.all().order_by('-created')

    context = {'room': room, 'room_messages': room_messages, 'participants': participants}
    return render(request, 'api/room.html', context)

@login_required(login_url='/login')
def create_room(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        # form = RoomForm(request.POST)
        topic_name = request.POST.get('topic')
        # If we don't have a niche/topic that the user wants, then he can add that. If it has not been created before created will be False.
        topic, created = Topic.objects.get_or_create(name=topic_name)
        Room.objects.create(
            host = request.user,
            topic = topic,
            name = request.POST.get('name'),
            description = request.POST.get('description'),
        )
        # if form.is_valid():
        #     room = form.save(commit=False)
        #     room.host = request.user
        #     room.save()
        return redirect('homepage')

    context = {'form': form, 'topics': topics, 'operation': 'Create'}
    return render(request, 'api/room_form.html', context)

@login_required(login_url='/login')
def update_room(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()

    if request.user != room.host:
        return HttpResponse('You are not allowed to update this Room!!')

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        # If we don't have a niche/topic that the user wants, then he can add that. If it has not been created before created will be False.
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('homepage')
        
    context = {'form': form, 'topics': topics, 'room': room, 'operation': 'Update'}
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

@login_required(login_url='/login')
def delete_message(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('You are not allowed to delete this Message!!')
    
    if request.method == 'POST':
        message.delete()
        return redirect('homepage')
    return render(request, 'api/delete.html', {'obj': message})

def user_profile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()

    rooms = Room.objects.all()
    room_count = rooms.count()

    context = {'user':user, 'rooms': rooms, 'room_messages': room_messages, 'topics': topics, 'room_count': room_count}
    return render(request, 'api/profile.html', context)

@login_required(login_url='login')
def update_user(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)

    context = {'form': form, 'user': user}
    return render(request, 'api/update_user.html', context)