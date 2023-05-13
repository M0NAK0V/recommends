from django.contrib import admin

# Register your models here.
from .models import Room, Topic, Message, Achievement, Course, Question

admin.site.register(Room)
admin.site.register(Topic)
admin.site.register(Message)
admin.site.register(Achievement)
admin.site.register(Course)
admin.site.register(Question)