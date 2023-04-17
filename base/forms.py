from django.forms import ModelForm
from .models import Room
from .models import Achievement
from .models import UserAchievement

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