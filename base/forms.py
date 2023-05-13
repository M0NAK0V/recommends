from django import forms
from django.forms import ModelForm
from .models import Room, Achievement, Course, Question, Option

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
    options = forms.ModelMultipleChoiceField(queryset=Option.objects.none())

    class Meta:
        model = Question
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance.question_type == 'text':
            del self.fields['options']
        else:
            self.fields['options'].queryset = Option.objects.filter(question=self.instance)

        if self.instance.pk:
            self.fields['options'].queryset = self.instance.options.all()
            self.fields['options'].widget = forms.CheckboxSelectMultiple() if self.instance.question_type == 'checkbox' else forms.RadioSelect()
