from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.db.models import Q, Sum
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm 
from .models import Room, Topic, Message, Achievement, Course, Question, CourseResult, BigCourse
from .forms import RoomForm, CourseForm, QuestionForm, BigCourseForm
from django.views.generic import ListView
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse



def results(request, pk):
    bigcourse = BigCourse.objects.get(id=pk)
    results = CourseResult.objects.all()
    context = {'results': results}
    return render(request, 'courses/results.html', context)

# class AchievementAdd(UserPassesTestMixin,CreateView):
#     model = UserAchievement
#     form_class = AchievementAdd
#     template_name = 'achievements/form2.html'
#     success_url = reverse_lazy('achievements-list')

#     def test_func(self):
#         return self.request.user.is_superuser
    
def bigcourse(request, pk):
    bigcourse = BigCourse.objects.get(id=pk)
    courses = Course.objects.filter(bigcourse=bigcourse)
    context = {'bigcourse': bigcourse, 'courses': courses}
    return render(request, 'courses/bigcourse.html', context)

def course(request, pk, pk_1):
    bigcourse = BigCourse.objects.get(id=pk)
    course = Course.objects.get(id=pk_1)
    questions = Question.objects.filter(course=course)
    context = {'course': course, 'questions': questions}
    return render(request, 'courses/course.html', context)

def bigcourses(request):
    bigcourses = BigCourse.objects.all()
    context = {'bigcourses': bigcourses}
    return render(request, 'courses/bigcourses.html', context)

def courses(request):
    courses = Course.objects.all()
    context = {'courses': courses}
    return render(request, 'courses/courses.html', context)

@login_required
def create_bigcourse(request):
    if request.method == 'POST':
        form = BigCourseForm(request.POST)
        if form.is_valid():
            bigcourse = form.save(commit=False)
            bigcourse.save()
            messages.success(request, 'BigCourse created successfully!')
            return redirect('bigcourses')
    else:
        form = BigCourseForm()
    context = {
        'form': form,
    }
    return render(request, 'courses/create_bigcourse.html', context)

@login_required
def create_course(request, pk):
    bigcourse = BigCourse.objects.get(id=pk)
    courses = Course.objects.filter(bigcourse=bigcourse)
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.save()
            total_progress = Course.objects.filter(bigcourse=bigcourse).aggregate(Sum('progress'))['progress__sum']
            bigcourse.progress = total_progress
            bigcourse.save()
            messages.success(request, 'Course created successfully!')
            return HttpResponseRedirect(reverse('course', args=[bigcourse.id,course.id]))
    else:
        form = CourseForm()
    context = {
        'bigcourse': bigcourse,
        'form': form,
    }
    return render(request, 'courses/create_course.html', context)

@login_required
def add_question(request, pk, pk_1):
    bigcourse = BigCourse.objects.get(id=pk)
    course = Course.objects.get(id=pk_1)
    questions = Question.objects.filter(course=course)
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.course = course  # set the course for the question
            question.save()
            form.save_m2m()
            total_points = Question.objects.filter(course=course).aggregate(Sum('points'))['points__sum']
            course.progress = total_points
            course.save()
            return HttpResponseRedirect(reverse('course', args=[bigcourse.id,course.id]))
    else:
        form = QuestionForm()
    context = {
        'bigcourse': bigcourse,
        'course': course,
        'form': form,
    }
    return render(request, 'courses/add_question.html', context)

@login_required
def update_question(request, pk, pk_1, pk_2):
    bigcourse = BigCourse.objects.get(id=pk)
    course = Course.objects.get(id=pk_1)
    questions = Question.objects.filter(course=course)
    question = Question.objects.get(id=pk_2)
    form = QuestionForm(instance=question)
    if request.user != question.user:
        return HttpResponse('ухади')
    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save(commit=False)
            question.course = course  # set the course for the question
            question.save()
            form.save_m2m()
            total_points = Question.objects.filter(course=course).aggregate(Sum('points'))['points__sum']
            course.progress = total_points
            course.save()
            return HttpResponseRedirect(reverse('course', args=[bigcourse.id,course.id]))
    else:
        form = QuestionForm()
    context = {
        'bigcourse': bigcourse,
        'course': course,
        'form': form,
    }
    return render(request, 'courses/update_question.html', context)

@login_required
def delete_question(request, pk, pk_1, pk_2):
    bigcourse = BigCourse.objects.get(id=pk)
    course = Course.objects.get(id=pk_1)
    questions = Question.objects.filter(course=course)
    question = Question.objects.get(id=pk_2)
    if request.user != question.user:
        return HttpResponse('ухади')
    if request.method == 'POST':
        question.delete()
        total_points = Question.objects.filter(course=course).aggregate(Sum('points'))['points__sum']
        course.progress = total_points
        course.save()
        return HttpResponseRedirect(reverse('course', args=[bigcourse.id,course.id]))
    else:
        form = QuestionForm()
    context = {
        'bigcourse': bigcourse,
        'course': course,
        'form': form,
    }
    return render(request, 'base/delete.html',{'obj':question})


@login_required
def course_questions(request, pk, pk_1):
    bigcourse = BigCourse.objects.get(id=pk)
    course = Course.objects.get(id=pk_1)
    questions = Question.objects.filter(course=course)
    return render(request, 'courses/course_questions.html', {'course': course, 'questions': questions})

@login_required
def course_solve(request, pk, pk_1):
    bigcourse = BigCourse.objects.get(id=pk)
    course = Course.objects.get(id=pk_1)
    questions = Question.objects.filter(course=course)

    if request.method == 'POST':
        score = 0

        for question in questions:
            answer = request.POST.get('answer_{}'.format(question.id))
            if answer.lower() == question.otvet.lower():
                score += question.points
        CourseResult.objects.create(user=request.user, course=course, score=score)

        return HttpResponseRedirect(reverse('course', args=[bigcourse.id,course.id]))

    return render(request, 'courses/course_solve.html', {'course': course, 'questions': questions})


    
# def update_achievement_progress(request, achievement_id):
#     achievement = get_object_or_404(Achievement, id=achievement_id)
#     course_id = request.POST.get('course')
#     if course_id:
#         course = get_object_or_404(Course, id=course_id)
#         progress = request.POST.get('progress', 0)
#         course.progress = progress
#         course.save()
#         achievement.progress = course.achievements.filter(id=achievement.id).count() / course.achievements.count() * 100
#         achievement.save()
#         messages.success(request, 'Achievement progress updated successfully!')
#     return redirect('achievement_list')

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
    # user_achievements = UserAchievement.objects.filter(user=request.user)
    context = {'user':user,'rooms':rooms,'room_messages':room_messages,'topics' : topics}
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