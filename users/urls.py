from django.urls import path
from users.views import UserpostView

urlpatterns = [
    path('/posts',UserpostView.as_view()),
]