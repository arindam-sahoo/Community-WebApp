from django.shortcuts import render

rooms = [
    {
        'id': 1,
        'name': 'Let\'s Test out Comms-ee'
    },
    {
        'id': 2,
        'name': 'Building the server with Python-Django'
    },
    {
        'id': 3,
        'name': 'Using HTML Templating now, gonna change to React later'
    }
]

def home(request):
    context = {'rooms': rooms}
    return render(request, 'api/home.html', context)

def room(request, pk):
    room = None
    for i in rooms:
        if i['id'] == int(pk):
            room = i
    
    context = {'room': room}
    return render(request, 'api/room.html', context)