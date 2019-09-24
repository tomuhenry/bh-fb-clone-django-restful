from django.db import models
from users.models import CustomUser
from posts.models import Post


class Comment(models.Model):
    author = models.ForeignKey(CustomUser, related_name='comments', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    comment_body = models.CharField(max_length=300)

    class Meta:
        ordering = ["-created_at", "-updated_at"]

    def __str__(self):
        return self.comment_body


