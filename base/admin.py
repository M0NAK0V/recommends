from django.contrib import admin

# Register your models here.
from .models import Room, Topic, Message, Achievement, Course, Question, CourseResult, BigCourse

admin.site.register(Room)
admin.site.register(Topic)
admin.site.register(Message)
admin.site.register(Achievement)
admin.site.register(BigCourse)
admin.site.register(Course)
admin.site.register(Question)
admin.site.register(CourseResult)