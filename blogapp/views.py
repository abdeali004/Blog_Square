from django.shortcuts import render,redirect
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.http import HttpResponse, request,JsonResponse
from django.contrib.auth import get_user
from django import forms
from django.db.models import Count
from django.template import RequestContext
from .models import Blog_article,Article_comment,Article_votes_description,Article_tag
from blogMain.models import userInfo
import datetime

class form(forms.Form):
    image = forms.ImageField()

def handler404(request, *args, **argv):
    response = render(request,'404.html', {})
    response.status_code = 404
    return response


def handler500(request, *args, **argv):
    response = render(request,'500.html', {})
    response.status_code = 500
    return response

# Create your views here.
def allblogs_view(request,pagenum):
    paginator = Paginator(Blog_article.get_all_blogs(),4)
    try:
        blogs = paginator.page(pagenum)
    except PageNotAnInteger:
        blogs = paginator.page(1)
    except EmptyPage:
        blogs = paginator.page(paginator.num_pages)

    latestposts = Blog_article.get_all_blogs().order_by("-blog_creation_date")
    alltags = Article_tag.get_all_tags().annotate(Count("count"))

    if (latestposts.count() > 4):
        latestposts = latestposts[0:3]

    if alltags.count() > 4:
        alltags = alltags[0:3]

    context = {
        "currdate":datetime.datetime.now(),
        "blogslist":blogs,
        "latest_posts": latestposts,
        "alltags" : alltags
    }
    return render(request, "blogs.html",context)

def blog_view(request,id):
    blog = Blog_article.get_blog(id)
    if(len(blog) > 0):
        blog = blog[0]
        tags = blog.blog_tags.split(",")
        latestposts = Blog_article.get_all_blogs().order_by("-blog_creation_date")
        alltags = Article_tag.get_all_tags().annotate(Count("count")).order_by('-count')
        
        if latestposts.count() > 4:
            latestposts = latestposts[0:3]

        if alltags.count() > 4:
            alltags = alltags[0:3]
        
        # increase blogViews
        if not request.user.is_anonymous:
            userIn = userInfo.objects.get(username=request.user)
            views = userIn.blogsViewed
            match = str(id) + ","
            if(match not in views):
                views += match
            userIn.blogsViewed = views
            userIn.save()

        context = {
            "tags":tags,
            "blog":blog,
            "latest_posts": latestposts,
            "alltags":alltags,
        }
        return render(request,"post.html",context)
    return render(request,"post.html")


def user_blog_creation_view(request,*args,**kwargs):
    context = {
        "imageform":form(),
    }
    return render(request,"addblog.html",context)

def getcomment(request,id):
    Blog_article.update_views(id)
    commentlist = Article_comment.get_article_comments(id)
    
    return JsonResponse(commentlist,safe=False)

def savecomment(request,id):
    if request.method == 'POST':
        user = request.POST.get('user')
        usercomment = request.POST.get('usercomment')
        userobj = userInfo.get_user(user)
        articleobj = Blog_article.get_blog(id)[0]
        Article_comment.savecomment(articleobj,userobj,usercomment)
        Blog_article.update_comment_count(id)
        userInfo.increment_comment(user)
        return JsonResponse({"user":user,"date":datetime.date.today(),"comment":usercomment},safe=True)

def votescounter(request):
    if request.method == "POST":
        like = request.POST.get('like')
        blogid = request.POST.get('blogid')
        user = request.POST.get('user')
        if like == "true":
            Blog_article.upvote(blogid,user)
        else:
            Blog_article.downvote(blogid,user)

        Article_votes_description.updateval(user,blogid,like)

    downvote =  Blog_article.get_downvotes_count(blogid)
    upvote   =  Blog_article.get_upvotes_count(blogid)
    return JsonResponse({"upvote":upvote,"downvote":downvote},safe=False)

def get_user_votes(request):
    if request.method == "POST":
        blog_id = request.POST.get('blog_id')
        user = request.POST.get('user')
        userIn = userInfo.objects.get(username = user)
        uservote = Article_votes_description.get_votes(blog_id).filter(user = userIn)
        like = False
        dislike = False
        if (uservote.count() != 0):
            like = uservote[0].like
            dislike = uservote[0].dislike    
    return JsonResponse({"like":like,"dislike":dislike},safe=False)
    

def added_blog_preview(request):
    if request.method == "POST":
        title = request.POST.get('title').capitalize()
        # thumbnail = request.POST.get('image')
        category = request.POST.get('category').capitalize()
        tags = request.POST.get('tags')
        tags = tags.split('#')[1:]
        tags = [tag.capitalize().strip() for tag in tags]

        content = request.POST.get('content')

        imageform = form(request.POST,request.FILES)
        imageform.is_valid()
        blogid = Blog_article.save_blog(request.user,title,imageform.cleaned_data['image'],category,tags,content)

        latestposts = Blog_article.get_all_blogs().order_by("-blog_creation_date")
    
        if latestposts.count() > 4:
            latestposts = latestposts[0:3]


        context = {
            "blog":Blog_article.get_blog(id = blogid)[0],
            "latest_posts":latestposts,
            "tags":tags,
            "preview":True
        }
        return render(request,"post.html",context)


def discard_changes(request,id):
    blogdata = Blog_article.get_blog(id)
    if(len(blogdata) > 0):
        blogdata = blogdata[0]
        context = {
            "title":blogdata.blog_title,
            "thumbnail":blogdata.blog_thumbnail,
            "category":blogdata.blog_category,
            "tags": blogdata.blog_tags,
            "content":blogdata.blog_content,
            "imageform": form() }
        blogdata.delete_blog(id)
        author = userInfo.objects.get(username=request.user)
        author.blogsPublished -= 1
        author.save()
        return render(request,"addblog.html",context)
    return redirect("/blogapp/create")


def show_liked_posts(request,user):
    likedposts = Article_votes_description.get_user_liked_posts(user)
    context = {
        "user": user,
        "likedposts":likedposts,
        "likecount":likedposts.count()
    }
    return render(request, "likedislike.html",context)

def search_view(request):
    if request.method == "POST":
        query = request.POST.get('search').capitalize()

        searchbytitle = Blog_article.objects.filter(blog_title__contains=query)
        searchbycategory = Blog_article.objects.filter(blog_category__contains=query)
        searchbytags = Blog_article.objects.filter(blog_tags__contains=query)
        searchbycontent = Blog_article.objects.filter(blog_content__contains=query)
        
        blogarr = set()
        if (searchbytitle.count()>0):
            for item in searchbytitle:
                if(item not in blogarr):
                    blogarr.add(item)

        if (searchbycategory.count()>0):
            for item in searchbycategory:
                if(item not in blogarr):
                    blogarr.add(item)

        if (searchbytags.count()>0):
             for item in searchbytags:
                if(item not in blogarr):
                    blogarr.add(item)

        if (searchbycontent.count()>0):
             for item in searchbycontent:
                if(item not in blogarr):
                    blogarr.add(item)
        

        latestposts = Blog_article.get_all_blogs().order_by("-blog_creation_date")
        alltags = Article_tag.get_all_tags().annotate(Count("count")).order_by('-count')

        if (latestposts.count() > 4):
            latestposts = latestposts[0:3]

        if alltags.count() > 4:
            alltags = alltags[0:3]


        print(blogarr)
        context = {
            "searchedblogs":blogarr,
            "latest_posts":latestposts,
            "alltags" : alltags,
        }


        return render(request, "search.html",context)


def category_search_view(request,category):
    category = category.capitalize()
    blogarr = []
    searchbycategory = Blog_article.objects.filter(blog_category=category)
    #blogarr.append(searchbycategory)

    latestposts = Blog_article.get_all_blogs().order_by("-blog_creation_date")
    alltags = Article_tag.get_all_tags().annotate(Count("count")).order_by('-count')

    if (latestposts.count() > 4):
        latestposts = latestposts[0:3]

    if alltags.count() > 4:
        alltags = alltags[0:3]

    noresult = False
    if (searchbycategory.count() == 0):
        noresult = True

    context = {
        "searchedblogs":searchbycategory,
        "latest_posts":latestposts,
        "alltags" : alltags,
        "noresult":noresult
    }

    return render(request, "search.html",context)

def tag_search_view(request,tag):
    tag = tag.capitalize()
    blogarr = []
    searchbytags = Article_tag.objects.filter(tags=tag)
    collectblogs = []
    if (searchbytags.count()>0):
            searchbytags = searchbytags[0].blog_id.split(',')
            for blogid in searchbytags:
                if(blogid == ''):
                    continue
                collectblogs.append(Blog_article.objects.filter(blog_id=blogid)[0])
            #blogarr.append(collectblogs)

    latestposts = Blog_article.get_all_blogs().order_by("-blog_creation_date")
    alltags = Article_tag.get_all_tags().annotate(Count("count")).order_by('-count')

    if (latestposts.count() > 4):
        latestposts = latestposts[0:3]

    if alltags.count() > 4:
        alltags = alltags[0:3]

    noresult = False
    if (len(collectblogs) == 0):
        noresult = True

    context = {
        "searchedblogs":collectblogs,
        "latest_posts":latestposts,
        "alltags" : alltags,
        "noresult":noresult
    }
    return render(request, "search.html",context)

    
def author_profile_view(request,author,allposts):        
    userobj = userInfo.objects.get(username=author)
    myblogs = Blog_article.get_user_blogs(userobj)

    if allposts == 0 and len(myblogs) > 4:
        myblogs = myblogs[0:4]

    context = {
        "myblogs":myblogs,
        "allposts":allposts,
        "authorname":userobj
    }
    return render(request,"myPosts.html",context)

        
