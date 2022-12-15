import json
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from django.core.paginator import Paginator

from .models import User, Post, Follow


def index(request):
    posts = Post.objects.all().order_by("id").reverse()

    # Pagination Feature
    p = Paginator(posts, 10)
    pageNumber = request.GET.get('page')
    postsPage = p.get_page(pageNumber)


    return render(request, "network/index.html", {
        "posts": posts,
        "postsPage": postsPage
    })


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

# Create New Post
def newPost(request):
    # POST request method
    if request.method == "POST":
        postField = request.POST["newPostText"]

        # Check who is the user
        user = request.user

        # Add data to the database
        createdPost = Post.objects.create(author=user, description=postField, like=0)

        # Save data to the database
        createdPost.save()

        return HttpResponseRedirect(reverse("index"))

# Profile Page
def profilePage(request, user_id):
    user = User.objects.get(pk=user_id) # User from the card
    posts = Post.objects.filter(author=user).order_by("id").reverse()

    # Following and Followers info for that user
    following = Follow.objects.filter(user=user)
    follower = Follow.objects.filter(followedUser=user)

    # Checking if the user is still following a specific person
    try:
        checkingFollow = follower.filter(user=User.objects.get(pk=request.user.id))
        if len(checkingFollow) != 0:
            isFollowing = True
        else:
            isFollowing = False

    except:
        isFollowing = False


    # Pagination Feature
    p = Paginator(posts, 10)
    pageNumber = request.GET.get('page')
    postsPage = p.get_page(pageNumber)

    return render(request, "network/profile.html", {
        "posts": posts,
        "p": p,
        "postsPage": postsPage,
        "username": user.username,
        "userProfile": user,
        "following": following,
        "follower": follower,
        "isFollowing": isFollowing
    })

# Follow Button from Profile Page
def follow(request):
    # Get info about the user from the Card (Inside Profile Page)
    userProfile = request.POST['userProfile']

    # Get the current user who logged in
    currentUser = User.objects.get(pk=request.user.id)

    # Check the username of the person (from User) who the current user wants to follow
    userProfileVerified = User.objects.get(username=userProfile)

    # Update the Follow database
    newFollow = Follow(user=currentUser, followedUser=userProfileVerified)
    newFollow.save()

    user_id = userProfileVerified.id
    
    return HttpResponseRedirect(reverse("profilePage", kwargs= {"user_id": user_id} ))

# Unfollow Button from Profile Page
def unfollow(request):
    # Get info about the user from the Card (Inside Profile Page)
    userProfile = request.POST['userProfile']

    # Get the current user who logged in
    currentUser = User.objects.get(pk=request.user.id)

    # Check the username of the person (from User) who the current user wants to unfollow
    userProfileVerified = User.objects.get(username=userProfile)

    # Update the Follow database
    newUnfollow = Follow.objects.get(user=currentUser, followedUser=userProfileVerified)
    newUnfollow.delete()

    user_id = userProfileVerified.id
    
    return HttpResponseRedirect(reverse("profilePage", kwargs= {"user_id": user_id} ))


# Following Page
def following(request):
    # Get the current user who logged in
    currentUser = User.objects.get(pk=request.user.id)
    followingUsers = Follow.objects.filter(user=currentUser)

    posts = Post.objects.all().order_by("id").reverse()

    followingPosts = []

    # Filter all posts, to just get the posts made by users that the current user follows
    for post in posts:
        for user in followingUsers:
            if user.followedUser == post.author:
                followingPosts.append(post)

    # Pagination Feature
    p = Paginator(followingPosts, 10)
    pageNumber = request.GET.get('page')
    postsPage = p.get_page(pageNumber)

    return render(request, "network/following.html", {
        "postsPage": postsPage
    })

# Edit Post Feature
def editPost(request, post_id):
    # POST request method
    if request.method == "POST":
        # Check textarea value
        data = json.loads(request.body)
        textarea_edit = Post.objects.get(pk=post_id)
        textarea_edit.description = data["description"]

        # Save new value from textarea  and return JsonResponse
        textarea_edit.save()
        return JsonResponse({
            "message": "Edit successfully",
            "data": data["description"]
        })