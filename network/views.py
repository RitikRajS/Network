from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
import json
from django.views.decorators.csrf import csrf_exempt

from .models import User, Post, Follow
from .forms import PostForm


def pagination(request, data):

    paginator=Paginator(data, 10)
    page_number= request.GET.get('page')

    data= paginator.get_page(page_number)

    # Total Number of pages needed for our requirement 
    totalpages= data.paginator.num_pages

    # Number of pages in a list

    pagelist=[n+1 for n in range(totalpages)]

    return (data, totalpages, pagelist)

    

@csrf_exempt
def index(request):


    if request.method == "GET":

        posts= Post.objects.all().order_by('-posted_date')

        # Like/Unliked Post 
        liked_users={}

        for liked in posts:
            liked_users[liked.id] = [user.username for user in liked.likes.all()]

 
        #Pagination 
        posts, totalpage, pagelist= pagination(request, posts)

        return render(request, "network/index.html", {
            "posts":posts,
            "totalpage":totalpage,
            "pagelist":pagelist,
            "likedUsers":liked_users,
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
    

@csrf_exempt
def post(request):

    """ TO SUBMIT A NEW POST"""

    if request.method == 'GET':

        #empty post form to submit a post
        post_form= PostForm()

        return render(request, "network/post.html", {
            'new_post':post_form
        })
    

    elif request.method == 'POST':


        if request.user.is_authenticated:


            form = PostForm(request.POST)

            if form.is_valid():

                post= form.save(commit=False)
                post.author = request.user
                post.save()
                return HttpResponseRedirect(reverse('index'))
            
        else:

            return HttpResponseRedirect(reverse('login_view'))
                

@csrf_exempt
def profile(request, name):

    """ TO VIEW A PROFILE OF A USER """

    try:

        # Creating the user object 
        user_object = User.objects.get(username= name)

    except User.DoesNotExist:
        return JsonResponse({"error": "Invalid Profile"}, status=400)


    if request.method=="GET":

        # Using the object to filter the name
        all_posts = Post.objects.filter(author=user_object)

        # Reverse Chronological order 
        all_posts = all_posts.order_by('-posted_date')

        # Users liking each post
        liked_users={}

        for liked in all_posts:
            liked_users[liked.id] = [user.username for user in liked.likes.all()]

        # Pagination Use
        all_posts, totalpage, pagelist= pagination(request, all_posts)

        # User Followers and Following

        follow_instance= Follow.objects.filter(user=user_object)

        # Follower

        follower_count =0 
        follower_list = []
        follower_name=[]

        for follow in follow_instance:
            follower_list.extend(follow.followers.all())
            follower_name.extend([follower.username for follower in follow.followers.all()])

        follower_count=len(follower_list)

        # Following 

        following_instance=Follow.objects.filter(followers=user_object)

        following_count= 0
        following_list=[]

        for following in following_instance:
            following_list.append(following.user)

        following_count= len(following_list)


        return render(request, 'network/profile.html', {
            "posts":all_posts,
            "totalpage":totalpage,
            "pagelist":pagelist,
            "user_details": user_object,
            "follower_count": follower_count,
            "follower_list": follower_list,
            "following_count": following_count,
            "following_list": following_list,
            "follower_name":follower_name,
            "likedUsers":liked_users,

        })
    
    elif request.method =="PUT":

        """ User sending a PUT request to add or remove following"""

        try:
            data=json.loads(request.body)
            follow_action= data.get('follow')

            follower_instance, created = Follow.objects.get_or_create(user=user_object)

            if follow_action:
                follower_instance.followers.add(request.user)
            
            else:
                follower_instance.followers.remove(request.user)

            follower_instance.save()

            return JsonResponse({
                'follower_count':follower_instance.followers.count()

            }, status=200)


        except Follow.DoesNotExist:
            return JsonResponse({'error': "Follow Instance does not exists"}, status=404)
            


@login_required
@csrf_exempt
def following(request):
    
    if request.method=="GET":
        
        if request.user.is_authenticated:

            following_query= Follow.objects.filter(followers= request.user)

            following_users=[]

            for follow in following_query:

                following_users.append(follow.user)

            following_posts= Post.objects.filter(author__in=following_users).order_by('-posted_date')

            # Like/Unliked Post 

            liked_users={}

            for liked in following_posts:
                liked_users[liked.id] = [user.username for user in liked.likes.all()]

            #Pagination 
            following_posts, totalpage, pagelist= pagination(request, following_posts)

            return render(request, 'network/following.html', {
                "posts":following_posts,
                "totalpage":totalpage,
                "pagelist":pagelist,
                "likedUsers":liked_users,
            })

        else:
            return HttpResponseRedirect(reverse('login'))


@csrf_exempt
@login_required
def edit(request, post_id):
    
    """PUT request to edit the post content"""

    if request.method=='PUT':
        
        try:
            data= json.loads(request.body)
            edited_content= data.get('content')

            if not edited_content:
                return JsonResponse({'error': 'Content cannot be empty'}, status= 400)

            # Post Instance 

            post_instance = Post.objects.get(id= post_id)

            post_instance.post_content= edited_content

            post_instance.save()

            return JsonResponse({
                'updated_content':post_instance.post_content

            }, status=200)


        except Post.DoesNotExist:
            return JsonResponse({'error': "Follow Instance does not exists"}, status=404)


@csrf_exempt
@login_required
def like(request, postID):

    if request.method == "PUT":
        
        try:
            data= json.loads(request.body)
            likeStatus= data.get('like')

            if likeStatus is None:
                return JsonResponse({'error: Invalid Status'}, status= 404)

            post_instance = Post.objects.get(id= postID)

            if likeStatus:
                post_instance.likes.add(request.user)

            else:
                post_instance.likes.remove(request.user)

            return JsonResponse({
                'updatedLikes':post_instance.likes.count()}, status=200)


        except Post.DoesNotExist:
            return JsonResponse({'error': "Follow Instance does not exists"}, status=404)

    
    




