from django.shortcuts import render,redirect
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.http import HttpResponse, request,JsonResponse
from django.contrib.auth import get_user
from .models import blog_article,article_comments,article_votes_description
from blogMain.models import userInfo
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

def blog_view(request,id):
    blog = blog_article.get_blog(id)
    context = {
        "blog":blog,
        "latest_posts":blog_article.get_all_blogs().order_by("-blog_creation_date")[0:3]
    }
    return render(request,"post.html",context)

def userblogs_view(request,allposts):
    userobj = get_user(request)
    if (len(userobj.username) == 0):
        return redirect("home")
        
    userobj = userInfo.objects.get(username=userobj.username)
    myblogs = blog_article.get_user_blogs(userobj)

    if allposts == 0 and len(myblogs) > 4:
        myblogs = myblogs[0:4]

    context = {
        "myblogs":myblogs,
        "allposts":allposts,
    }
    return render(request,"myPost.html",context)

def createblog_view(request):
    pass

def getcomment(request,id):
    blog_article.update_views(id)
    commentlist = article_comments.get_article_comments(id)
    return JsonResponse(commentlist,safe=False)

def savecomment(request,id):
    if request.method == 'POST':
        user = request.POST.get('user')
        usercomment = request.POST.get('usercomment')
        userobj = userInfo.get_user(user)
        articleobj = blog_article.get_blog(id)
        article_comments.savecomment(articleobj,userobj,usercomment)
        blog_article.update_comment_count(id)
        return JsonResponse({"user":user,"date":datetime.date.today(),"comment":usercomment},safe=True)

def votescounter(request):
    if request.method == "POST":
        like = request.POST.get('like')
        blogid = request.POST.get('blogid')
        plus = request.POST.get('plus')
        if like == "true":
            blog_article.upvote(blogid,plus)
        else:
            blog_article.downvote(blogid,plus)

        votesdescobj = article_votes_description.updateval(request.user,blogid,like)

    downvote =  blog_article.get_downvotes_count(blogid)
    upvote   =  blog_article.get_upvotes_count(blogid)
    return JsonResponse({"upvote":upvote,"downvote":downvote},safe=False)

def get_user_votes(request):
    if request.method == "POST":
        blog_id = request.POST.get('blog_id')
        uservote = article_votes_description.get_votes(blog_id)
        like = False
        dislike = False
        if (uservote.count() != 0):
            like = uservote[0].like
            dislike = uservote[0].dislike    
    return JsonResponse({"like":like,"dislike":dislike},safe=False)

    