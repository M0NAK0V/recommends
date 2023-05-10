from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm 
from .models import Room, Topic, Message, Achievement, UserAchievement, Course
from .forms import RoomForm, AchievementForm, AchievementAdd, CourseForm
from django.views.generic import ListView
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import UserPassesTestMixin


class AchievementList(ListView):
    model = Achievement
    template_name = 'achievements/list.html'
    context_object_name = 'achievements'

class CourseList(ListView):
    model = Course
    template_name = 'achievements/courses_list.html'
    context_object_name = 'courses'



class AchievementCreate(UserPassesTestMixin,CreateView):
    model = Achievement
    form_class = AchievementForm
    template_name = 'achievements/form.html'
    success_url = reverse_lazy('achievements-list')

    def test_func(self):
        return self.request.user.is_superuser
    
class AchievementAdd(UserPassesTestMixin,CreateView):
    model = UserAchievement
    form_class = AchievementAdd
    template_name = 'achievements/form2.html'
    success_url = reverse_lazy('achievements-list')

    def test_func(self):
        return self.request.user.is_superuser
    
def create_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.save()
            messages.success(request, 'Course created successfully!')
            return redirect('courses-list')
    else:
        form = CourseForm()
    return render(request, 'achievements/create_course.html', {'form': form})

def update_achievement_progress(request, achievement_id):
    achievement = get_object_or_404(Achievement, id=achievement_id)
    course_id = request.POST.get('course')
    if course_id:
        course = get_object_or_404(Course, id=course_id)
        progress = request.POST.get('progress', 0)
        course.progress = progress
        course.save()
        achievement.progress = course.achievements.filter(id=achievement.id).count() / course.achievements.count() * 100
        achievement.save()
        messages.success(request, 'Achievement progress updated successfully!')
    return redirect('achievement_list')

# rooms = [
#    {'id': 1, 'name': 'Name1'},
#    {'id': 2, 'name': 'Name2'},
#    {'id': 3, 'name': 'Name3'},
# ]
# Create your views here.
def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
             messages.error(request, 'Пользователь отсутствует')
        
        user = authenticate(request, username=username,password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Пользователь или пароль не существуют')
    context ={'page':page}
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user= form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request, 'Ошибка во время реги')
    return render(request, 'base/login_register.html', {'form':form})

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
                                Q(topic__name__icontains=q) |
                                Q(name__icontains=q)|
                                Q(description__icontains=q)
                                )
    topics = Topic.objects.all()
    room_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))
    context = {'rooms':rooms, 'topics': topics, 'room_count':room_count,
               'room_messages':room_messages}
    return render(request, 'base/home.html', context)

def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    participants = room.participants.all()
    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)
    
    context = {'room': room, 'room_messages':room_messages, 'participants':participants}
    return render(request, 'base/room.html', context)

def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    user_achievements = UserAchievement.objects.filter(user=request.user)
    context = {'user':user,'rooms':rooms,'room_messages':room_messages,'topics' : topics, 'user_achievements': user_achievements}
    return render(request, 'base/profile.html', context)

@login_required(login_url='/login')
def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        # print(request.POST)
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.host = request.user
            room.save()
            return redirect('home')


    context = {'form': form}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='/login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse('ухади')
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='/login')
def deleteRoom(request,pk):
    room = Room.objects.get(id=pk)
    if request.user != room.host:
        return HttpResponse('ухади')
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html',{'obj':room})

@login_required(login_url='/login')
def deleteMessage(request,pk):
    message = Message.objects.get(id=pk)
    if request.user != message.user:
        return HttpResponse('ухади')
    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'base/delete.html',{'obj':message})