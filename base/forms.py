from django import forms
from django.forms import ModelForm
from .models import Room, Achievement, Course, Question

class RoomForm(ModelForm):
    class Meta:
        model = Room 
        fields = '__all__'
        exclude = ['host','participants']


class CourseForm(ModelForm):
    class Meta:
        model = Course
        fields = '__all__'
        exclude = ['completion_date','progress']

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = '__all__'
