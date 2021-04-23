from django.contrib import admin
from django.urls import path,include
import blogMain.views as views
# from blogapp.views import allblogs_view ,blog_view ,userblogs_view
import blogapp
from blogapp import urls as blogurls

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
    path('blogapp/',include(blogurls)),
    path('contact', views.contact, name = "contact"),
    path('user_help', views.user_help, name="help"),
    path('about', views.about, name = "about"),
]