from django.db import models
from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):
    last_request = models.DateTimeField(auto_now_add=True)


class Post(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField("date published", auto_now_add=True)
    author = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name="posts"
    )

    def __str__(self):
        return self.text

    class Meta:
        ordering = ("-pub_date",)


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    pub_date = models.DateTimeField("date published", auto_now_add=True)

    class Meta:
        unique_together = ("user", "post")
