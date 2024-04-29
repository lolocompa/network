from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage
import json
from django.views.decorators.csrf import csrf_exempt


from .models import User, post, follows
page_num = 1
profile_num = 1
following_num = 1

def index(request):
    global page_num

    if request.method == "GET":
        current_user = request.user
        all_post = post.objects.all()
        page_posts = load_page_index(page_num, all_post)

        return render(request, "network/index.html", {
            "all_posts": page_posts,
            "current_user": current_user,
            "page_num": page_num
        })
    else:
        p_or_n = request.POST.get("p_or_n")
        if p_or_n == "next":
            page_num += 1
            return HttpResponseRedirect(reverse("index"))
        else:
            page_num -= 1
            return HttpResponseRedirect(reverse("index"))




def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")




def make_post(request):
    if request.method == "GET":
        return render(request, "network/make_post.html")
    else:
        user = request.user
        content = request.POST.get("content")
        new_post = post(user=user, content=content)
        new_post.save()
        return HttpResponseRedirect(reverse("index"))


def edit_post(request, post_id):
    if request.method == "GET":
        this_post = post.objects.get(pk = post_id)
        return render(request, "network/edit_post.html", {
            "this_post": this_post
        })
    else:
        this_post = post.objects.get(pk = post_id)
        new_content = request.POST.get("content")
        this_post.content = new_content
        this_post.save()
        return HttpResponseRedirect(reverse("index"))


def profile(request, user):
    global profile_num

    if request.method == "GET":
        user_to = User.objects.get(username=user)
        user_posts = post.objects.filter(user=user_to)
        page_user = load_page_profile(profile_num, user_posts)

        followers = follows.objects.filter(follow_user=user_to)
        i_follow = follows.objects.filter(user=user_to)

        followers_count = followers.count()
        i_follow_count = i_follow.count()

        is_following = follows.objects.filter(user=request.user, follow_user= user_to )
        
        return render(request, "network/profile.html", {
            "user": user,
            "user_posts": page_user,
            "followers_count": followers_count,
            "i_follow_count": i_follow_count,
            "current_user": str(request.user),
            "page_num": profile_num,
            "is_following": is_following
        } )
    else:
        p_or_n = request.POST.get("p_or_n")
        if p_or_n == "next":
            profile_num += 1
            return HttpResponseRedirect(reverse("profile", args=[user]))
        else:
            profile_num -= 1
            return HttpResponseRedirect(reverse("profile", args=[user]))
        




    


def load_page_index(index, all_posts):
    global page_num
    p = Paginator(all_posts, 10)
    try:
        page = p.page(index)
        return page
    except EmptyPage:
        page = p.page(1)
        page_num = 1
        return page
    

def load_page_profile(index, all_posts):
    global profile_num
    p = Paginator(all_posts, 10)
    try:
        page = p.page(index)
        return page
    except EmptyPage:
        page = p.page(1)
        profile_num = 1
        return page
    

def load_page_following(index, all_posts):
    global following_num
    p = Paginator(all_posts, 10)
    try:
        page = p.page(index)
        return page
    except EmptyPage:
        page = p.page(1)
        following_num = 1
        return page


@csrf_exempt
def get_post(request, post_id):
    this_post = post.objects.get(pk = post_id)

    if request.method == "GET":
         return JsonResponse(this_post.serialize())
    elif request.method == "PUT":
        data = json.loads(request.body)
        if data.get("is_liked") is not None:
            this_post.is_liked = data["is_liked"]
        if data.get("likes") is not None:
            this_post.likes = data["likes"]
        this_post.save()
        return HttpResponse(status=204)



def follow(request):
    if request.method == "POST":
        follow_value = request.POST.get("follow")

        if follow_value == "follow":
            current_user = request.POST.get("current_user")
            user = request.POST.get("user")

            user_object1 = User.objects.get(username=current_user)
            user_object2 = User.objects.get(username=user)

            
            new_follow = follows(user=user_object1, follow_user=user_object2)
            new_follow.save()
            return HttpResponseRedirect(reverse("profile", args=[user]))

        else:
            current_user_delete = request.POST.get("current_user")
            user_delete = request.POST.get("user")

            user_delete_object1 = User.objects.get(username=current_user_delete)
            user_delete_object2 = User.objects.get(username=user_delete)
            
            delete_follow = follows.objects.filter(user=user_delete_object1, follow_user=user_delete_object2)
            delete_follow.delete()
            return HttpResponseRedirect(reverse("profile", args=[user_delete]))

            


def following(request):
    global following_num
    if request.method == "GET":
        current_user = request.user
        this_user = User.objects.get(username=current_user)

        all_following_people = follows.objects.filter(user=this_user).values_list("follow_user", flat=True)
        all_following_posts = post.objects.filter(user__in=all_following_people)
        if not all_following_posts:
            return render(request, "network/following.html", {
            "message": "you dont follow anyone"
        })
        page_posts = load_page_following(following_num, all_following_posts)

        return render(request, "network/following.html", {
            "user_posts": page_posts
        })
    else:
        p_or_n = request.POST.get("p_or_n")
        if p_or_n == "next":
            following_num += 1
            return HttpResponseRedirect(reverse("following"))
        else:
            following_num -= 1
            return HttpResponseRedirect(reverse("following"))

