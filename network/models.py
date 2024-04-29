from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass


class follows(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="this_user_follows")
    follow_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_being_followed")


class post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField(null=False)
    likes = models.IntegerField(default=0)
    is_liked = models.BooleanField(default=False)

    def __str__(self):
        return f"user: {self.user}, timestamp: {self.timestamp}, content: {self.content}, likes: {self.likes}"

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user.username,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
            "content": self.content,
            "likes": self.likes,
            "is_liked": self.is_liked
        }