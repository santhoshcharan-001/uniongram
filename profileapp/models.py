from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class posts(models.Model):
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=100)
    like_count = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)
    time_stamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title

class comments(models.Model):
    content = models.TextField()
    time_stamp = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(posts, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.content

class likes(models.Model):
    post_id = models.ForeignKey(posts, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    time_stamp = models.DateTimeField(auto_now_add=True)

    # def __str__(self):
    #     return self.like_id

class follows(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='follower')
    followee = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='following')
    time_stamp = models.DateTimeField(auto_now_add=True)
