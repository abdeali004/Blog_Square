from django.contrib import admin
from .models import blog_article,article_comments,article_votes_description

# Register your models here.
admin.site.register(blog_article)
admin.site.register(article_comments)
admin.site.register(article_votes_description)