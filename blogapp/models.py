from django.db import models
from blogMain.models import userInfo
import random

# Create your models here.
class Blog_article(models.Model):
    def upload_thumbnail(self,filename):
        val = random.randint(1,99)
        return f'blog_thumbnails/{self.blog_author}_{self.blog_id}/{val}_{filename}'

    blog_id = models.CharField(max_length=255)
    blog_title = models.CharField(max_length=255)
    blog_thumbnail = models.ImageField(upload_to=upload_thumbnail,default="{static 'img/blog_thumbnail_default.jpg'}")
    blog_creation_date = models.DateTimeField(auto_now_add=True)
    blog_category = models.CharField(max_length = 20)
    blog_tags = models.TextField(default="")
    num_of_comments = models.IntegerField(default=0)
    blog_views = models.IntegerField(default=0)
    blog_upvote = models.IntegerField(default=0)
    users_upvote = models.TextField(default="")
    blog_downvote = models.IntegerField(default=0)
    users_downvote = models.TextField(default="")
    blog_author = models.ForeignKey(userInfo,null = True,on_delete=models.SET_NULL)
    blog_content = models.TextField()

    def __str__(self):
        return str(self.blog_id)

    @staticmethod
    def get_user_blogs(user):
        return Blog_article.objects.filter(blog_author = user)

    @staticmethod
    def get_all_blogs():
        return Blog_article.objects.all()

    @staticmethod
    def get_blog(id):
        return Blog_article.objects.filter(blog_id = id)

    @staticmethod
    def update_comment_count(id):
        commentcount = Blog_article.objects.get(blog_id=id).num_of_comments
        Blog_article.objects.filter(blog_id=id).update(num_of_comments = commentcount+1)

    @staticmethod
    def update_views(id):
        blogviews = Blog_article.objects.get(blog_id=id).blog_views
        Blog_article.objects.filter(blog_id=id).update(blog_views = blogviews + 1)

    @staticmethod
    def upvote(id,user):
        match = str(user) + ","
        userIn = userInfo.objects.get(username=user)
        userIn.blogsLiked += 1
        userIn.save()
        blog = Blog_article.objects.get(blog_id=id)
        if(match not in blog.users_upvote):
            if(match in blog.users_downvote):
                blog.blog_downvote = blog.blog_downvote - 1
                blog.users_downvote = blog.users_downvote.replace(match, "")
                blog.blog_upvote = blog.blog_upvote + 1
                blog.users_upvote = blog.users_upvote + match
            else:
                blog.blog_upvote = blog.blog_upvote + 1
                blog.users_upvote = blog.users_upvote + match
            blog.save()

    @staticmethod
    def downvote(id,user):
        match = str(user) + ","
        userIn = userInfo.objects.get(username=user)
        userIn.blogsLiked -= 1
        userIn.save()
        blog = Blog_article.objects.get(blog_id=id)
        if(match not in blog.users_downvote):
            if(match in blog.users_upvote):
                blog.blog_upvote = blog.blog_upvote - 1
                blog.users_upvote = blog.users_upvote.replace(match, "")
                blog.blog_downvote = blog.blog_downvote + 1
                blog.users_downvote = blog.users_downvote + match
            else:
                blog.blog_downvote = blog.blog_downvote + 1
                blog.users_downvote = blog.users_downvote + match
            blog.save()


    @staticmethod
    def get_downvotes_count(blogid):
        return Blog_article.objects.get(blog_id=blogid).blog_downvote

    @staticmethod
    def get_upvotes_count(blogid):
        return Blog_article.objects.get(blog_id=blogid).blog_upvote

    @staticmethod
    def save_blog(user,title,thumbnail,category,tags,content):
        author = userInfo.objects.get(username=user)
        count = author.blogsCount+1
        blogid = str(user) + '#' + str(count)
        keywords = ','.join(tags)
        author.blogsCount = count
        author.blogsPublished += 1
        author.save()
        newblog = Blog_article.objects.create(blog_id=blogid, blog_title=title,blog_thumbnail=thumbnail,blog_category=category,
        blog_tags=keywords,blog_content = content,blog_author=author)
        newblog.save()
        #article tags creation
        for tag in tags:
            if tag:
                tagobj = Article_tag.get_tagobj(tag)
                if tagobj.count() == 0:
                    Article_tag.create_tagobj(tag,blogid)
                else:
                    Article_tag.update_tagobj(tag,tagobj[0].count,tagobj[0].blog_id + "," + blogid)
        return blogid



    @staticmethod
    def delete_blog(id):
        tags = Blog_article.objects.get(blog_id=id).blog_tags
        tags = tags.split(',')
        for tag in tags:
            if tag:
                Article_tag.deletetag(tag,id)

        Blog_article.objects.get(blog_id = id).delete()


class Article_comment(models.Model):
    blog_id = models.ForeignKey(Blog_article,on_delete=models.CASCADE)
    comment_author = models.ForeignKey(userInfo,on_delete=models.CASCADE)
    comment_content = models.CharField(max_length=300)
    comment_creation_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.comment_author) + "-" + str(self.blog_id)

    @staticmethod 
    def get_article_comments(id):
        allcomments = Article_comment.objects.values()
        blogIn = Blog_article.objects.get(blog_id = id).id
        allcomments = [comment for comment in allcomments if (comment['blog_id_id'] == blogIn)]
        return allcomments

    @staticmethod
    def savecomment(blog,user,comment):
        obj = Article_comment(blog_id = blog,comment_author=user,comment_content=comment)
        obj.save()



class Article_tag(models.Model):
    tags = models.CharField(max_length=100)
    count = models.IntegerField()
    blog_id = models.CharField(max_length=255)

    def __str__(self):
        return self.tags

    @staticmethod
    def create_tagobj(tag,blogid):
        Article_tag.objects.create(tags=tag,count=1,blog_id=blogid)

    @staticmethod
    def update_tagobj(tag,countval,newblogid):
        Article_tag.objects.filter(tags=tag).update(count = countval + 1,blog_id= newblogid)

    @staticmethod
    def get_tagobj(tag):
        return Article_tag.objects.filter(tags=tag)

    @staticmethod
    def deletetag(tag,blogid):
        tagobj = Article_tag.objects.get(tags=tag)
        newcount = tagobj.count - 1
        if newcount == 0:
            tagobj.delete()
        else:
            safe_blog = tagobj.blog_id.split(',')
            safe_blog = [blog for blog in safe_blog if blog != blogid]
            safe_blog = ",".join(safe_blog)
            tagobj.update_tagobj(tag,newcount-1,safe_blog)

    @staticmethod
    def get_all_tags():
        return Article_tag.objects.all()
    
class Article_votes_description(models.Model):
    user = models.ForeignKey(userInfo,on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog_article,on_delete=models.CASCADE)
    like = models.BooleanField(default=False)
    dislike = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user) + "-" + str(self.blog)

    @staticmethod
    def updateval(username,blog_id,like):
        user = userInfo.objects.get(username=username)
        blog = Blog_article.objects.get(blog_id=blog_id)

        if like == "true":
            Article_votes_description.objects.update_or_create(user=user,blog=blog,defaults = {"like":True,"dislike":False})
        else:
            Article_votes_description.objects.update_or_create(user=user,blog=blog,defaults = {"like":False,"dislike":True})

    @staticmethod
    def get_votes(id):
        blog = Blog_article.objects.get(blog_id=id)
        return Article_votes_description.objects.filter(blog=blog)

    @staticmethod
    def get_user_liked_posts(username):
        userIn = userInfo.objects.get(username = username)
        return Article_votes_description.objects.filter(user=userIn).filter(like = True)