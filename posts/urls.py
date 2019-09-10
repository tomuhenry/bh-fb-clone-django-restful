from django.urls import path

from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.PostListView.as_view(), name='list_post'),
    path('<int:pk>/', views.PostRetrieveUpdateDestroyView.as_view(), name='post_detail'),
]
