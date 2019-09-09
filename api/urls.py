from django.urls import include, path

urlpatterns = [
    path('users/', include('users.urls', namespace='users')),
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/signup/', include('rest_auth.registration.urls')),
    path('posts/', include('posts.urls', namespace='posts')),
]
