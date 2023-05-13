from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm 
from .models import Room, Topic, Message, Achievement, Course, Question, CourseResult
from .forms import RoomForm, CourseForm, QuestionForm
from django.views.generic import ListView
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse



    
# class AchievementAdd(UserPassesTestMixin,CreateView):
#     model = UserAchievement
#     form_class = AchievementAdd
#     template_name = 'achievements/form2.html'
#     success_url = reverse_lazy('achievements-list')

#     def test_func(self):
#         return self.request.user.is_superuser
    

def course(request, pk):
    course = Course.objects.get(id=pk)
    questions = Question.objects.filter(course=course)
    context = {'course': course, 'questions': questions}
    return render(request, 'courses/course.html', context)

def courses(request):
    courses = Course.objects.all()
    context = {'courses': courses}
    return render(request, 'courses/courses.html', context)

@login_required
def create_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.save()
            messages.success(request, 'Course created successfully!')
            return redirect('courses')
    else:
        form = CourseForm()
    return render(request, 'courses/create_course.html', {'form': form})

@login_required
def add_question(request, pk):
    course = Course.objects.get(id=pk)
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.course = course  # set the course for the question
            question.save()
            form.save_m2m()
    else:
        form = QuestionForm()
    context = {
        'course': course,
        'form': form,
    }
    return render(request, 'courses/add_question.html', context)


@login_required
def course_questions(request, pk):
    course = Course.objects.get(id=pk)
    questions = Question.objects.filter(course=course)
    return render(request, 'courses/course_questions.html', {'course': course, 'questions': questions})

@login_required
def course_solve(request, pk):
    course = Course.objects.get(id=pk)
    questions = Question.objects.filter(course=course)

    if request.method == 'POST':
        score = 0

        for question in questions:
            answer = request.POST.get('answer_{}'.format(question.id))

            if question.question_type == "text":
                if answer.lower() == question.answer.lower():
                    score += question.points
            else:
                answers = request.POST.getlist('answer_{}[]'.format(question.id))
                correct_options = question.options.filter(is_correct=True)
                correct_option_ids = [option.id for option in correct_options]
                answers_ids = [int(id) for id in answers]

                if set(correct_option_ids) == set(answers_ids):
                    score += question.points

        CourseResult.objects.create(user=request.user, course=course, score=score)

        return HttpResponseRedirect(reverse('course_solve', args=[course.id]))

    return render(request, 'courses/course_solve.html', {'course': course, 'questions': questions})

# @login_required
# def answers(request, pk):
#     course = Course.objects.get(id=pk)
#     questions = course.question_set.all()
#     answers = {}
#     if request.method == 'POST':
#         for question in questions:
#             answer = request.POST.get(f'question_{question.id}')
#             if answer:
#                 answers[question.id] = answer.strip()
#     context = {
#         'course': course,
#         'questions': questions,
#         'answers': answers,
#     }
#     if request.method == 'POST':
#         correct_answers = {}
#         for question in questions:
#             correct_answers[question.id] = question.otvet
#         if answers == correct_answers:
#             context['success'] = 'Вы успешно решили курс!'
#         else:
#             context['error'] = 'Вы допустили ошибку в решении курса'
#     return render(request, 'courses/answers.html', context)


    
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
    courses = Course.objects.filter(
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