from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .models import Room, Topic
from .forms import RoomForm

# Create your views here.


# rooms = [
#     {'id': 1, 'name': 'learn!'},
#     {'id': 2, 'name': 'design!'},
#     {'id': 3, 'name': 'develop!'},
# ]

def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist.')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password does not exist.')

    context = {'page':page}
    return render(request, 'mainapp/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration')

    return render(request, 'mainapp/login_register.html', {'form': form})
def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )

    topics = Topic.objects.all()
    room_count = rooms.count()

    context = {'rooms': rooms, 'topics': topics, 'room_count': room_count}
    return render(request, 'mainapp/home.html', context)

def room(request, pk):
    room = Room.objects.get(id=pk)
    participants = room.participants.all()
    if request.method == 'POST':

        room.participants.add(request.user)
        return redirect('room', pk=room.id)

    context = {'room': room, 'participants': participants}
    return render(request, 'mainapp/room.html', context)

@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()

    # if request.user != room.host:
    #     return HttpResponse('You are not allowed here')

    if request.method == 'POST':
        form = RoomForm(request.POST, request.FILES)
        if form.is_valid():
            room = form.save(commit=False)
            room.host = request.user  # Устанавливаем хоста как текущего пользователя
            room.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'mainapp/room_form.html', context)

@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse('You are not allowed here')

    if request.method == 'POST':
        form = RoomForm(request.POST, request.FILES, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'mainapp/room_form.html', context)

@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse('You are not allowed here')

    if request.method == 'POST':
        room.delete()
        return redirect('home')

    return render(request, 'mainapp/delete.html', {'obj': room})
