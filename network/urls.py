
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("make_post", views.make_post , name="make_post"),
    path("edit_post/<int:post_id>", views.edit_post, name="edit_post"),
    path("profile/<str:user>", views.profile, name="profile"),
    path("follow", views.follow, name="follow"),
    path("following", views.following, name="following"),


    #api
    path("posts/<int:post_id>", views.get_post, name="get_post"),
    path("profile/posts/<int:post_id>", views.get_post, name="get_post")
]
