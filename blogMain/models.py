from django.db import models
import random
from django.contrib.auth.models import User

# Create your models here.
def user_directory_path1(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    i = random.randint(1,1000)
    ext = filename.split('.')[-1]
    return 'userImages/{0}{1}+.{2}'.format(instance.username,i, ext)


class userInfo(models.Model):
    username = models.CharField(primary_key=True, max_length=50)
    email = models.EmailField(max_length=254)
    typeOf = models.CharField(max_length=50,default="")
    gender = models.CharField(max_length=50)
    categories = models.CharField(max_length=150)
    pic = models.ImageField(upload_to=user_directory_path1, height_field=None, width_field=None, max_length=None, default="userImages/defaultShow.jpg")
    fb = models.TextField(default="")
    insta = models.TextField(default="")
    city = models.CharField(max_length=50,default="")
    state = models.CharField(max_length=50,default="")
    postal = models.CharField(max_length=50,default="")
    about = models.TextField(default="")
    blogsViewed = models.TextField(default="")
    blogsPublished = models.IntegerField(default=0)
    blogsCount = models.IntegerField(default=0)
    visitedSite = models.IntegerField(default=0)
    commented = models.IntegerField(default=0)
    blogsLiked = models.IntegerField(default=0)
    newUser = models.BooleanField(default=True)
    checkCode = models.CharField(max_length=12)
    date = models.DateTimeField(auto_now=False, auto_now_add=True)

    @staticmethod
    def get_user(user):
        return userInfo.objects.get(username = user)
    
    @staticmethod
    def increment_comment(user):
        obj = userInfo.objects.filter(username = user)
        if(len(obj) > 0):
            obj = obj[0]
            obj.commented = obj.commented + 1
            obj.save()


    def __str__(self):
        return self.username


class verifyUser(models.Model):
    username = models.CharField(max_length=50)
    email = models.EmailField(primary_key=True, max_length=254)
    full_name = models.CharField(max_length=100)
    verificationCode = models.CharField(max_length=12)

    def __str__(self):
        return self.email