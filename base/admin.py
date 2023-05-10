from django.contrib import admin

# Register your models here.
from .models import Room, Topic, Message, Achievement, UserAchievement, Course

admin.site.register(Room)
admin.site.register(Topic)
admin.site.register(Message)
admin.site.register(Achievement)
admin.site.register(UserAchievement)
admin.site.register(Course)