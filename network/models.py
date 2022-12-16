from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    author = models.ForeignKey("User", on_delete=models.CASCADE, related_name="user")
    description = models.CharField(max_length=1000)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id}: {self.author}"

class Follow (models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="user_follows")
    followedUser = models.ForeignKey("User", on_delete=models.CASCADE, related_name="followed_user")

    def __str__(self):
        return f"{self.user} follows {self.followedUser}"

class Like (models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, default='', related_name="user_like")
    post = models.ForeignKey("Post", on_delete=models.CASCADE, default='', related_name="post_like")

    def __str__(self):
        return f"{self.id}:{self.user} likes {self.post}"