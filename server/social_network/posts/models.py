from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

class MyUser(AbstractUser):
    last_action = models.DateTimeField(blank=True, null=True)


class Post(models.Model):
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='posts', related_query_name='posts')
    title = models.CharField(max_length=40)
    text = models.TextField()
    likes = models.ManyToManyField(MyUser, through='Like', blank=True)


class Like(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    date_created = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'post']
