from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.

class UserProfileInfo(models.Model):

    user = models.OneToOneField(User,on_delete=models.CASCADE)
    #additional
    portfolio_site = models.URLField(blank=True)
    profile_pic = models.ImageField(upload_to='profile_pic', blank=True)

    def __str__(self):
        return self.user.username


class Post(models.Model):
    author = models.CharField(max_length=50)
    title = models.CharField(max_length=200)
    content = models.CharField(max_length=3000)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True,null=True)

    def __str__(self):
        return self.author or self.content
    
    # def __str__(self):
    #     return self.published_date


    def published_date(self):
        return self.published_date == timezone.now()
        self.save()
