from django.urls import path
from users.views import UserPostView, UserPostDetailView

urlpatterns = [
    path('/posts',UserPostView.as_view()),
    path('/posts/<int:post_num>',UserPostDetailView.as_view()),
]