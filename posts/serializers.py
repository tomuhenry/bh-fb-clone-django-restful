from rest_framework import serializers
from . import models
from users.serializers import UserSerializer


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(many=False, read_only=True)

    class Meta:
        model = models.Post
        fields = ('author', 'created_at', 'post_body', )
