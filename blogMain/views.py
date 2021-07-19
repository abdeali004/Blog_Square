from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from blogMain.models import userInfo, verifyUser
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth import get_user
import json
import random
from django.template.loader import get_template
from django.core.mail import EmailMessage
from django.conf import settings
from django.db.models import Count
from datetime import datetime,date
from blogapp.models import Blog_article,Article_comment,Article_votes_description,Article_tag

# Create your views here.
def home(request):
    loginCheck = False
    if not request.user.is_anonymous:
        loginCheck = True
        author = userInfo.objects.get(username=request.user)
        author.blogsPublished = 2
        author.blogsCount = 3
        author.save()
    trendingblogs = Blog_article.get_all_blogs().annotate(Count('blog_upvote')).order_by("-blog_upvote")
    latestblogs = Blog_article.get_all_blogs().order_by("-blog_creation_date")
    
    if (trendingblogs.count() > 2):
        trendingblogs = trendingblogs[0:2]
    if (latestblogs.count() > 4):
        latestblogs = latestblogs[0:4]

    context = {
                "loginCheck" : loginCheck,
                "trendingblogs": trendingblogs,
                "latestblogs": latestblogs
            }
    return render(request, "index.html",context)

@csrf_exempt
def registerUser(request):
    if request.method == "POST":
        userName = request.POST.get(
            "username").lower()
        userMail = request.POST.get(
            "email")
        userPass = request.POST.get("password")
        userFullName = request.POST.get("fullname")
        user1 = User.objects.filter(username=userName)
        user2 = User.objects.filter(email=userMail)
        if len(user1) == 0 and len(user2) == 0:
            userData = verifyUser.objects.filter(email=userMail)
            if userData:
                verifyUser.objects.get(email=userMail).delete()
            verifyCode = random.choice(
                ["b", "l", "o", "g", "s", "q", "r"]) + str(random.randint(100000, 1000000))
            verifyUser.objects.create(
                username=userName, full_name=userFullName, email=userMail, verificationCode=verifyCode)
            heading = "Blog Square account request."
            messageContent = "Your blogSquare account's secret verification code : " + verifyCode
            msg = EmailMessage(heading, messageContent, settings.EMAIL_HOST_USER,
                               [userMail, ])
            msg.send()
            context = {
                "username": userName,
                "password": userPass,
                "email": userMail,
                "fullname": userFullName,

            }
            return render(request, "verify.html", context)

        elif user1:
            messages.warning(
                request, 'Username already taken. Please Sign Up using another username.')
            return redirect("/login")
        else:
            messages.warning(
                request, 'E-mail already taken. Please Sign Up using another E-mail.')
            return redirect("/login")
    elif not request.user.is_anonymous:
        return redirect("/home")

    return render(request, "login.html")


def userVerify(request):
    if request.method == "POST":
        userName = request.POST.get("username").lower()
        userPass = request.POST.get("password")
        userMail = request.POST.get("email")
        userFullName = request.POST.get("fullname")
        code = request.POST.get("code")
        userData = verifyUser.objects.get(email=userMail)
        orgCode = userData.verificationCode
        if code == orgCode:
            verifyUser.objects.get(email=userMail).delete()
            user = User.objects.create_user(
                username=userName, password=userPass)
            user.first_name = userFullName
            user.email = userMail
            user.is_superuser = False
            user.save()
            # creating user info
            checkCodeValue = userName[:4] + "-" + \
                str(random.randint(11111, 100000))
        
            userInfo.objects.create(
                username=userName, email=userMail, checkCode=checkCodeValue)
            messages.info(
                request, 'You are registered successfully. Please Login to continue.')
            return redirect("/login")
        else:
            messages.warning(
                request, 'Verification failed!! Your verification code doesn\'t match, try again.')
            return redirect("/login")
    return render(request, "login.html")


def loginUser(request):
    if request.method == "POST":
        name = request.POST.get(
            "username").lower()
        userPass = request.POST.get("password")
        if name.__contains__("@"):
            exist = User.objects.filter(email=name)
            if exist:
                name = User.objects.get(email=name).username
            else:
                # No backend authenticated the credentials
                messages.warning(
                    request, 'Wrong Username or Password.')
                return render(request, "login.html")

        user = User.objects.filter(username=name)
        if user:
            user = authenticate(
                username=name, password=userPass)
            if user is not None:
                login(request, user)
                userchoice = userInfo.objects.filter(username=name)
                if len(userchoice):
                    userchoice = userInfo.objects.get(username=name)
                    userchoice.visitedSite += 1
                    userchoice.save()
                    if(userchoice.typeOf == ""):
                        return render(request, "person.html")
                    return redirect("/home")
            else:
                # No backend authenticated the credentials
                messages.warning(
                    request, 'Wrong Username or Password.')
                return render(request, "login.html")
        else:
            # No backend authenticated the credentials
            messages.warning(
                request, 'Username not registered! Please SignUp for a new account.')
            return render(request, "login.html")

    elif not request.user.is_anonymous:
        return redirect("/home")

    return render(request, "login.html")

@csrf_exempt
def forgotPage(request, page):
    if page == 1:
        return render(request, "forgotPage.html")
    elif page == 2:
        if request.method == "POST":
            emailin = request.POST.get("mail")
            userdata = userInfo.objects.filter(email=emailin)
            if userdata:
                code = userdata[0].checkCode
                heading = "Blog Square Password Change request."
                messageContent = "Your unique code : " + code
                msg = EmailMessage(heading, messageContent, settings.EMAIL_HOST_USER,
                                   [emailin, ])
                msg.send()
                context = {
                    "mail": emailin,

                }
                return render(request, "confirmPage.html", context)
            else:
                messages.warning(
                    request, 'Email not found. Please check and try again.')
                return redirect("/login")
        return redirect("/login")

    elif page == 3:
        if request.method == "POST":
            emailin = request.POST.get("mail")
            codeGet = request.POST.get("coded")
            userdata = userInfo.objects.filter(email=emailin)
            if userdata:
                code = userdata[0].checkCode
                if code == codeGet:
                    context = {
                        "mail": emailin,
                    }
                    return render(request, "passPage.html", context)
                else:
                    messages.warning(
                        request, 'Code is incorrect. Please try again and enter the new provided code.')
                    return redirect("/login")
            else:
                messages.warning(
                    request, 'No user found with the email. Please check and try again.')
                return redirect("/login")
            return redirect("/login")
        return redirect("/login")
    elif page == 4:
        if request.method == "POST":
            emailin = request.POST.get("mail")
            password = request.POST.get("newpass")
            userdata = userInfo.objects.get(email=emailin)
            userName = userdata.username
            checkCodeValue = userName[:4] + "-" + \
                str(random.randint(11111, 100000))
            userdata.checkCode = checkCodeValue
            userdata.save()
            u = User.objects.get(email=emailin)
            u.set_password(password)
            u.save()
            messages.success(
                request, 'Congratulations! Password changed successfully. LogIn to continue')
            return redirect("/login")
        return redirect("/login")
    else:
        return redirect("/login")



def logoutUser(request):
    if request.user.is_anonymous:
        return redirect("/login")
    logout(request)
    messages.info(
        request, 'You Logout Successfully. Come back soon.')
    return redirect("/login")

def ajaxStartupDetails(request):
    if request.user.is_anonymous:
        value = "false"
    # print(request.user)
    username = request.user
    typeOf = request.POST.get('typeOf', None)
    gender = request.POST.get('gender', None)
    categories = request.POST.get('category', None)
    userchoice = userInfo.objects.filter(username=username)[0]
    print(userchoice.typeOf)
    if(userchoice.typeOf != ""):
        value = "already"
    else:
        userchoice.typeOf = typeOf
        userchoice.categories = categories
        userchoice.gender = gender
        userchoice.save()
        value = "true"
    data1 = {
        'successful': value,
    }

    return JsonResponse(data1, safe=False)

def profile(request):
    if request.user.is_anonymous:
        return redirect("/login")
    profile = {}
    user = userInfo.objects.get(username=request.user)
    userUp = User.objects.get(username=request.user)
    profile["username"] = request.user
    profile["email"] = userUp.email
    name = userUp.get_full_name().split()
    profile["firstName"] = name[0]
    if len(name) > 1:
        profile["lastName"] = "".join(name[1:])
    typeOf = user.typeOf
    profile["pic"] = user.pic
    profile["fb"] = user.fb
    profile["insta"] = user.insta
    profile["city"] = user.city
    profile["state"] = user.state
    profile["postal"] = user.postal
    profile["about"] = user.about
    profile["visited"] = user.visitedSite
    profile["read"] = user.blogsCount
    profile["published"] = user.blogsPublished
    context = {
        "profile" : profile,
        "typeOf" : typeOf,
    }

    return render(request,"myProfile.html",context)

def profileEdit(request):
    if request.user.is_anonymous:
        value = "false"
    # print(request.user)
    first = request.POST.get('first', None)
    last = request.POST.get('last', None)
    fb = request.POST.get('fb', None)
    insta = request.POST.get('insta', None)
    city = request.POST.get('city', None)
    state = request.POST.get('state', None)
    postal = request.POST.get('postal', None)
    about = request.POST.get('about', None)

    user = userInfo.objects.get(username=request.user)
    userUp = User.objects.get(username=request.user)

    userUp.first_name = first
    userUp.last_name = last
    user.fb = fb.strip()
    user.insta = insta.strip()
    user.postal = postal
    user.city = city
    user.state = state
    user.about = about

    user.save()
    userUp.save()
    value = "true"
    data1 = {
        'successful': value,
    }

    return JsonResponse(data1, safe=False)

def updateImage(request):
    if request.method == "POST" and not request.user.is_anonymous:
        pic = request.FILES.get('pic')
        user = userInfo.objects.get(username=request.user)
        user.pic = pic
        user.save()
        print("done")
        return redirect("/myProfile")
    return redirect("/home")

def user_profile_main(request,username):
    target = str(username) + "/0"
    return redirect(target)

def user_profile(request,username, allposts):
    userobj = userInfo.objects.filter(username=username)
    if (len(userobj) == 0):
        return redirect("home")
    userobj = userobj[0]
    total_comments = userobj.commented
    total_blogs = userobj.blogsPublished
    total_views = len(userobj.blogsViewed.split(",")) - 1
    total_liked = userobj.blogsLiked
    myblogs = Blog_article.get_user_blogs(userobj)
    if ((allposts==0) and (len(myblogs)>4)):
        myblogs = myblogs[0:4]

    contribution = {
        "like": total_liked,
        "views": total_views,
        "published": total_blogs,
        "comments": total_comments
    }

    context = {
        "myblogs":myblogs,
        "allposts":allposts,
        "authorname":userobj,
        "contribution" : contribution,
    }
    return render(request,"myPosts.html",context)

def contact(request):
    return render(request, "contact.html")

def user_help(request):
    
    name = request.POST.get('name')
    email = request.POST.get('email')
    heading = request.POST.get('heading')
    message = request.POST.get('message')

    ctx = {
            'name': name,
            'email': email,
            'heading': heading,
            'message': message,
        }
    messageContent = get_template('mailTemplate.html').render(ctx)
    msg = EmailMessage(heading, messageContent, settings.EMAIL_HOST_USER, ["blogsquare.official@gmail.com", ])
    msg.content_subtype = 'html'
    msg.send()

    value = "true"
    data1 = {
        'successful': value,
    }
    return JsonResponse(data1, safe=False)

def about(request):
    return render(request, "about.html")

