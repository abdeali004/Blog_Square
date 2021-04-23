from django.shortcuts import render
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.http import HttpResponse, request
from .models import blog_article
import datetime

# Create your views here.
def allblogs_view(request,pagenum):
    paginator = Paginator(blog_article.get_all_blogs(),4)
    try:
        blogs = paginator.page(pagenum)
    except PageNotAnInteger:
        blogs = paginator.page(1)
    except EmptyPage:
        blogs = paginator.page(paginator.num_pages)

    context = {
        "currdate":datetime.datetime.now(),
        "blogslist":blogs,
        "latest_posts":blog_article.get_all_blogs().order_by("-blog_creation_date")[0:3]
    }
    return render(request, "blog.html",context)

def blog_view(request):
    pass

def userblogs_view(request):
    pass

def createblog_view(request):
    pass