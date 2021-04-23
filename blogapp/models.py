from django.db import models
from blogMain.models import userInfo

# Create your models here.
class blog_article(models.Model):
    def upload_thumbnail(self,filename):
        return '/blog_thumbnails/filename'

    blog_id = models.IntegerField(auto_created=True)
    blog_title = models.CharField(max_length=100)
    blog_thumbnail = models.ImageField(upload_to=upload_thumbnail,default="img/blog-2.jpg")
    blog_creation_date = models.DateTimeField(auto_now_add=True)
    blog_category = models.CharField(max_length = 20)
    blog_tags = models.TextField(default="")
    num_of_comments = models.IntegerField(default=0)
    blog_views = models.IntegerField(default=0)
    blog_upvote = models.IntegerField(default=0)
    blog_downvote = models.IntegerField(default=0)
    blog_author = models.ForeignKey(userInfo,null = True,on_delete=models.SET_NULL)
    blog_content = models.TextField()

    @staticmethod
    def get_all_blogs():
        return blog_article.objects.all()




class article_comments(models.Model):
    blog_id = models.ForeignKey(blog_article,on_delete=models.CASCADE)
    comment_author = models.ForeignKey(userInfo,on_delete=models.CASCADE)
    comment_content = models.CharField(max_length=300)
    comment_creation_date = models.DateTimeField(auto_now_add=True)



    

