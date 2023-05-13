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

class Achievement(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='achievements/')
    progress = models.IntegerField(default=0)
    achieved = models.ManyToManyField(User, related_name='achieved')
    def __str__(self):
        return self.name

class Course(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null = True)
    name = models.CharField(max_length=100)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null = True)
    description = models.TextField(max_length=255, default='')
    created_date = models.DateField(auto_now_add=True)
    completion_date = models.DateField(null=True, blank=True)
    progress = models.IntegerField(default=0) 
    def __str__(self):
        return self.name


class Question(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete= models.CASCADE)
    name = models.CharField(max_length=100)
    vopros = models.TextField(default='')
    otvet = models.TextField(default='')
    question_type = models.CharField(max_length=100, default='')
    options = models.ManyToManyField('Option')
    points = models.IntegerField(default=1)
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        super(Question, self).save(*args, **kwargs)
        self.options.clear()
        for option in self.options.all():
            self.options.add(option)
    
class Option(models.Model):
    text = models.CharField(max_length=100)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text
    
class CourseResult(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete= models.CASCADE)
    score = models.IntegerField(default=0)

    def __str__(self):
        return self.user