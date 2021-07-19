from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    path('blogs/<int:pagenum>',views.allblogs_view, name = "blogs"),
    path('blog/<str:id>', views.blog_view, name = "blog"),
    path('getcomment/<str:id>',views.getcomment,name="getcomment"),
    path('savecomment/<str:id>',views.savecomment,name="savecomment"),
    path('likesanddislikes/',views.votescounter,name="likes&dislikes"),
    path('getuservotes/',views.get_user_votes,name="uservotes"),
    path('create/',views.user_blog_creation_view,name="addblog"),
    path('previewing/',views.added_blog_preview,name="preview"),
    path('discard/<str:id>',views.discard_changes,name="discardpost"),
    path('liked/<str:user>',views.show_liked_posts,name="likedposts"),
    path('search/',views.search_view, name = "search"),
    path('categorysearch/<str:category>',views.category_search_view, name = "categorysearch"),
    path('tagsearch/<str:tag>',views.tag_search_view, name = "tagsearch"),
    path('author/profile/<str:author>/<int:allposts>',views.author_profile_view,name="authorprofile"),
] + static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)