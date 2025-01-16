from django.db import models
from django.contrib.auth.models import User



class UserDetails(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(null=True, default="avatar.svg")
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    avatar = models.ImageField(null=True, default="avatar.svg")
    college_name = models.CharField(max_length=200, blank=True, null=True)
    department_name = models.CharField(max_length=100, blank=True, null=True)
    current_year = models.PositiveIntegerField(blank=True, null=True)
    linkedin_url = models.URLField(blank=True, null=True)
    github_url = models.URLField(blank=True, null=True)
    twitter_url = models.URLField(blank=True, null=True)
    other_links = models.JSONField(blank=True, null=True) 
    avatar = models.ImageField(null=True, default="avatar.svg")
    def __str__(self):
        return f"{self.user.username} Details"
    

class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Room(models.Model):
    host = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    topic =models.ForeignKey(Topic,on_delete=models.SET_NULL,null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True,blank=True)
    participants = models.ManyToManyField(User,related_name='participants',blank=True)
    updated = models.DateTimeField(auto_now=True)
    created  = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated','-created']
    

    def __str__(self):
        return self.name
    

class Message(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    room = models.ForeignKey(Room,on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created  = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated','-created']
    

    def __str__(self):
        return self.body[0:50]
    
