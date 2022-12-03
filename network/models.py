from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Like(models.Model):
    like = models.IntegerField()

    def __str__(self):
        return f"{self.like}"

class Post(models.Model):
    author = models.ForeignKey("User", on_delete=models.CASCADE, related_name="user")
    description = models.CharField(max_length=1000)
    timestamp = models.DateTimeField(auto_now_add=True)
    like = models.IntegerField()

    def __str__(self):
        return f"{self.id}: {self.author}"



