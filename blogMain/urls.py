from django.contrib import admin
from django.urls import path
import blogMain.views as views

urlpatterns = [
    path('', views.home),
    path('home', views.home, name = "home"),
    path('login', views.loginUser, name = "login"),
    path('register', views.registerUser, name = "login"),
    path('verification', views.userVerify, name = "verification"),
    path('forgotPass/<int:page>', views.forgotPage, name='forgotPage'),
    path('logout', views.logoutUser, name="logout"),
    path('startupDetails', views.ajaxStartupDetails),
    path('myProfile', views.profile, name = "profile"),
    path('profileEdit', views.profileEdit),
    path('updateImage', views.updateImage, name="updateImage"),
    path('blogs', views.blogs, name = "blogs"),
    path('blog', views.blog, name = "blog"),
    path('userBlogs', views.userBlogs, name = "userBlogs"),
    path('contact', views.contact, name = "contact"),
    path('user_help', views.user_help, name="help"),
    path('about', views.about, name = "about"),
]