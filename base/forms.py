from django.forms import ModelForm
from .models import Room, Achievement, UserAchievement, Course

class RoomForm(ModelForm):
    class Meta:
        model = Room 
        fields = '__all__'
        exclude = ['host','participants']

class AchievementForm(ModelForm):
    class Meta:
        model = Achievement
        fields = ['name', 'description', 'image']
    
class AchievementAdd(ModelForm):
    class Meta:
        model = UserAchievement
        fields = ['user', 'achievement']

class CourseForm(ModelForm):
    class Meta:
        model = Course
        fields = '__all__'
        exclude = ['completion_date','progress']