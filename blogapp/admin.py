from django.contrib import admin
from .models import Blog_article,Article_comment,Article_votes_description,Article_tag

# Register your models here.
admin.site.register(Blog_article)
admin.site.register(Article_comment)
admin.site.register(Article_votes_description)
admin.site.register(Article_tag)