from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from posts.permissions import IsOwnerOrReadOnly

from .models import Comment
from posts.models import Post
from .serializers import CommentSerializer


class CommentListView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def post(self, request, *args, **kwargs):
        """ This method gets all comments for a post """
        serializer = CommentSerializer(data=request.data)
        post_pk = self.kwargs['post_pk']
        post = Post.objects.get(pk=post_pk)
        if serializer.is_valid():
            serializer.save(author=request.user, post=post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, *args, **kwargs):
        """ This method gets all comments for a post """
        post_pk = self.kwargs['post_pk']
        post = get_object_or_404(Post, pk=post_pk)
        comments = self.queryset.filter(post=post.pk)
        serializer = self.serializer_class(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CommentRetrieveDestroyView(generics.RetrieveDestroyAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

