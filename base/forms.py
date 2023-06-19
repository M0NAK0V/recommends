from django import forms
from django.forms import ModelForm
from .models import Room, Achievement, Course, Question, BigCourse

class RoomForm(ModelForm):
    class Meta:
        model = Room 
        fields = '__all__'
        exclude = ['host','participants']


class BigCourseForm(ModelForm):
    class Meta:
        model = BigCourse
        fields = '__all__'
        exclude = ['host','full_progress','min_progress','course_count']

class CourseForm(ModelForm):
    class Meta:
        model = Course
        fields = '__all__'
        exclude = ['host','completion_date','progress', 'min_progress', 'bigcourse']

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = '__all__'
        exclude = ['user','bigcourse','course']
