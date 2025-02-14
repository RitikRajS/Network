from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime


class User(AbstractUser):
    user_pfp = models.URLField(max_length=5000 , blank=True) 
    pass


class Post(models.Model):
    post_content = models.CharField(max_length=300)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    posted_date = models.DateTimeField(default=datetime.now)
    likes = models.ManyToManyField(User, blank=True, related_name="liked")

    def __str__(self):
        return(f'{self.author} posted {self.post_content} at {self.posted_date}')


class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_followed")
    followers = models.ManyToManyField(User, blank=True, related_name="follow_list")

    def __str__(self):
        follower_list= ','.join([follower.username for follower in self.followers.all()])
        return(f'{follower_list} started following {self.user.username}')

    
