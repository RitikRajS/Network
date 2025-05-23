
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("post", views.post, name="post"),
    path("following", views.following, name='following'),

    #API calls URL 
    path("profile/<str:name>", views.profile, name='profile'),
    path("edit/<int:post_id>", views.edit, name='edit'),
    path("like/<int:postID>", views.like, name='like'),

]
