from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from itertools import chain
import random

from .models import Profile, Post, LikePost, FollowesCount

# Create your views here.

@login_required(login_url='signin')
def index(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)

    like_post = LikePost.objects.all()

    user_following_list = []
    feed = []

    user_following = FollowesCount.objects.filter(follower=request.user.username)

    for user in user_following:
        user_following_list.append(user.user)

    for username in user_following_list:
        user = User.objects.get(username=username)
        profile = Profile.objects.get(user=user)
        feed_lists = Post.objects.filter(user=profile)
        feed.append(feed_lists)

    feed_list = list(chain(*feed))

    all_users = User.objects.all()
    user_following_all = []

    for user in user_following:
        user_list = User.objects.get(username=user.user)
        user_following_all.append(user_list)

    new_suggestions_list = [x for x in list(all_users) if x not in list(user_following_all)]
    current_user = User.objects.filter(username=request.user.username)
    final_suggestion_list = [x for x in list(new_suggestions_list) if x not in list(current_user)]
    random.shuffle(final_suggestion_list)

    username_profile = []
    username_profile_list = []

    for user in final_suggestion_list:
        username_profile.append(user.id)

    for id in username_profile:
        profile_lists = Profile.objects.filter(id_user=id)
        username_profile_list.append(profile_lists)

    suggestions_username_profile_list = list(chain(*username_profile_list))

    return render(request, 'index.html', {'user_profile': user_profile, 'posts': feed_list, 'like_post': like_post, 'suggestions_username_profile_list': suggestions_username_profile_list[:4]})

@login_required(login_url='signin')
def settings(request):
    user_profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':

        if request.FILES.get('image') == None:
            image = user_profile.profileimg
        if request.FILES.get('image') != None:
            image = request.FILES.get('image')

        bio = request.POST['bio']
        location = request.POST['location']

        user_profile.profileimg = image
        user_profile.bio = bio
        user_profile.location = location
        user_profile.save()

        return redirect('settings')

    return render(request, 'setting.html', {'user_profile': user_profile})

def signup(request):

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, "Email taken")
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, "Username taken")
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)

                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()
                return redirect('settings')
        else:
            messages.info(request, "Password not matching")
            return redirect('signup')
    return render(request, 'signup.html')
    
def signin(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Credentials invalid')
            return redirect('signin')
    
    return render(request, 'signin.html')

@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect('signin')

@login_required(login_url='signin')
def upload(request):
    
    if request.method == "POST":
        user = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user)
        image = request.FILES.get('image_upload')
        caption = request.POST['caption']

        new_post = Post.objects.create(user=user_profile, image=image, caption=caption)
        new_post.save()
    
    return redirect('/')

@login_required(login_url='signin')
def like_post(request):
    user = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user)
    post_id = request.GET.get('post_id')

    post = Post.objects.get(id=post_id)

    like_filter = LikePost.objects.filter(post_id=post_id, username=user_profile).first()

    if like_filter == None:
        new_like = LikePost.objects.create(post_id=post_id, username=user_profile)
        new_like.save()
        post.no_of_likes = post.no_of_likes + 1
    else:
        like_filter.delete()
        post.no_of_likes = post.no_of_likes - 1

    post.save()
    return redirect('/')

@login_required(login_url='signin')
def profile(request, pk):
    user_object = User.objects.get(username=pk)
    user_profile = Profile.objects.get(user=user_object)
    user_posts = Post.objects.filter(user=user_profile)
    user_post_length = len(user_posts)

    follower = request.user.username
    user = pk
    if FollowesCount.objects.filter(follower=follower, user=user).first():
        button_text = 'Unfollow'
    else:
        button_text = 'Follow'

    user_followers = len(FollowesCount.objects.filter(user=pk))
    user_following = len(FollowesCount.objects.filter(follower=pk))

    context = {
        'user_object': user_object,
        'user_profile': user_profile,
        'user_posts': user_posts,
        'user_post_length': user_post_length,
        "button_text": button_text,
        'user_followers': user_followers,
        'user_following': user_following
    }
    return render(request, 'profile.html', context)

@login_required(login_url='signin')
def follow(request):
    if request.method == 'POST':
        follower = request.POST['follower']
        user = request.POST['user']

        if FollowesCount.objects.filter(follower=follower, user=user).first():
            delete_follower = FollowesCount.objects.get(follower=follower, user=user)
            delete_follower.delete()
        else:
            new_follower = FollowesCount.objects.create(follower=follower, user=user)
            new_follower.save()

        return redirect('/profile/'+user)

    else:
        return redirect('/')

@login_required(login_url='signin')
def search(request):

    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)

    if request.method == 'POST':
        username = request.POST['username']
        username_object = User.objects.filter(username__icontains=username)

        username_profile = []
        user_profile_list = []

        for user in username_object:
            username_profile.append(user.id)

        for id in username_profile:
            profile_lists = Profile.objects.filter(id_user=id)
            user_profile_list.append(profile_lists)

        user_profile_list = list(chain(*user_profile_list))

    return render(request, 'search.html', {'user_profile': user_profile, 'user_profile_list': user_profile_list})