from django.urls import path

from . import views
from comments.views import CommentListView, CommentRetrieveDestroyView

app_name = 'posts'

urlpatterns = [
    path('', views.PostListView.as_view(), name='list_post'),
    path('<int:pk>/', views.PostRetrieveUpdateDestroyView.as_view(), name='post_detail'),
    path('<int:post_pk>/comments/', CommentListView.as_view(), name='list_comment'),
    path('<int:post_pk>/comments/<int:pk>', CommentRetrieveDestroyView.as_view(), name='comment_detail')
]
