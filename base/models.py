from django.db import models
from django.contrib.auth.models import User


class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    

# Create your models here.
class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null = True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null = True)
    name = models.CharField(max_length=200)
    description = models.TextField(null = True, blank = True)
    participants = models.ManyToManyField(User, related_name='participants',blank = True)
    updated = models.DateTimeField(auto_now = True)
    created = models.DateTimeField(auto_now_add = True)

    class Meta:
        ordering=['-updated', '-created']
    
    def __str__(self):
        return self.name

class Message(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete= models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now = True)
    created = models.DateTimeField(auto_now_add = True)
    class Meta:
        ordering=['-updated', '-created']
    
    def __str__(self):
        return self.body[0:50]

class Course(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=255, default='')
    created_date = models.DateField(auto_now_add=True)
    completion_date = models.DateField(null=True, blank=True)
    progress = models.IntegerField(default=0) 

class Achievement(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='achievements/')
    progress = models.IntegerField(default=0)
    courses = models.ManyToManyField(Course, related_name='achievements')
    def __str__(self):
        return self.name
    
class UserAchievement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    date_achieved = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.user.username + ' - ' + self.achievement.name
    