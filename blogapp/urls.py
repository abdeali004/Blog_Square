from django.contrib import admin
from django.urls import path,include
# from blogapp.views import allblogs_view ,blog_view ,userblogs_view
from . import views

urlpatterns = [
    path('blogs/<int:pagenum>',views.allblogs_view, name = "blogs"),
    path('blog/<int:id>', views.blog_view, name = "blog"),
    path('userBlogs/<int:allposts>', views.userblogs_view, name = "userBlogs"),
    path('',views.createblog_view,name="create"),
    path('getcomment/<int:id>',views.getcomment,name="getcomment"),
    path('savecomment/<int:id>',views.savecomment,name="savecomment")
]