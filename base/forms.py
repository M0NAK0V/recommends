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
        exclude = ['full_progress','min_progress']

class CourseForm(ModelForm):
    class Meta:
        model = Course
        fields = '__all__'
        exclude = ['completion_date','progress', 'min_progress']

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = '__all__'
