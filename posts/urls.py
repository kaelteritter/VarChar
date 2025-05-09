from django.urls import path

from posts import views


app_name = 'posts'

urlpatterns = [
    path('', views.home, name='home'),
    path('posts/<int:post_id>/', views.post_detail, name='post_detail'),
    path('posts/<int:post_id>/comment/', views.create_comment, name='create_comment'),
]
