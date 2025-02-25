from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import *
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.http import Http404
from django.contrib import messages
from django.urls import reverse
from django.db.models import Count
from a_posts.forms import ReplyCreateForm
from a_inbox.forms import InboxMessageForm
from a_posts .models import Post
# from itertools import chain
# import random
# Create your views here.
def profile_view(request,username=None):
    if username:
        profile=get_object_or_404(User,username=username).profile
      
    else:
        try:
           profile=request.user.profile
        except:
            raise Http404()
    posts=profile.user.posts.all()
    replyform=ReplyCreateForm()
    
    if request.htmx:
        if 'top-posts' in request.GET:
            posts=profile.user.posts.annotate(num_likes=Count('likes')).filter(num_likes__gt=0).order_by('-num_likes')
        elif 'top-comments' in request.GET:
            comments=profile.user.comments.annotate(num_likes=Count('likes')).filter(num_likes__gt=0).order_by('-num_likes')
            return render(request,'snippets/loop_profile_comments.html',{'comments':comments,'replyform':replyform})
        elif 'liked-posts' in request.GET:
            posts=profile.user.likedposts.order_by('-likedpost__created')
        return render(request,'snippets/loop_profile_posts.html',{'posts':posts})
            
    new_message_form=InboxMessageForm()
    context={
        'profile':profile,
        'posts':posts,
        'new_message_form':new_message_form
        
    }
    return render(request,'a_users/profile.html',context)
# def profile_view(request,username=None):
       
   
#     if username:
#         profile=get_object_or_404(User,username=username).profile
#     else:
#         try:
#            profile=request.user.profile
#         except:
#             raise Http404()
#     posts=profile.user.posts.all()
#     replyform=ReplyCreateForm()
    
#     if request.htmx:
#         if 'top-posts' in request.GET:
#             posts=profile.user.posts.annotate(num_likes=Count('likes')).filter(num_likes__gt=0).order_by('-num_likes')
#         elif 'top-comments' in request.GET:
#             comments=profile.user.comments.annotate(num_likes=Count('likes')).filter(num_likes__gt=0).order_by('-num_likes')
#             return render(request,'snippets/loop_profile_comments.html',{'comments':comments,'replyform':replyform})
#         elif 'liked-posts' in request.GET:
#             posts=profile.user.likedposts.order_by('-likedpost__created')
#         return render(request,'snippets/loop_profile_posts.html',{'posts':posts})
            
#     new_message_form=InboxMessageForm()
    
#     try:
#         user_object = get_object_or_404(User, username=username)
#         user_profile = get_object_or_404(Profile, user=user_object)
#     except Http404:
#         raise Http404("User not found")

#     # user_posts=Post.objects.filter(user=author)
#     # user_post_length=len(user_posts )  
#     context={
#         'profile':profile,
#         'posts':posts,
#         'new_message_form':new_message_form,
#         'user_profile':user_profile,
#         # 'user_posts':user_posts,
#         # 'user_post_length':user_post_length,
#         # 'user_object':user_object 
        
#     }
#     return render(request,'a_users/profile.html',context)

@login_required
def profile_edit_view(request):
    form =ProfileForm(instance=request.user.profile)
    if request.method=="POST":
        form =ProfileForm(request.POST,request.FILES,instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    if request.path == reverse('profile-onboarding'):
            template='a_users/profile_onboarding.html'
    else:
            template='a_users/profile_edit.html'
    return render(request, template,{'form':form})

@login_required
def profile_delete_view(request):
    user=request.user
    if request.method=="POST":
        logout(request)
        user.delete()
        messages.success(request,"Account deleted,What a pity")
        return redirect('home')
        
    return render (request,'a_users/profile_delete.html')

# def index(request):
#     user_object = User.objects.get(username=request.user.username)
#     user_profile = Profile.objects.get(user=user_object)

#     user_following_list = []
#     feed = []

#     user_following = FollowerCount.objects.filter(follower=request.user.username)

#     for users in user_following:
#         user_following_list.append(users.user)

#     for usernames in user_following_list:
#         feed_lists = Post.objects.filter(user=usernames)
#         feed.append(feed_lists)

#     feed_list = list(chain(*feed))

#     # user suggestion starts
#     all_users = User.objects.all()
#     user_following_all = []

#     for user in user_following:
#         user_list = User.objects.get(username=user.user)
#         user_following_all.append(user_list)
    
#     new_suggestions_list = [x for x in list(all_users) if (x not in list(user_following_all))]
#     current_user = User.objects.filter(username=request.user.username)
#     final_suggestions_list = [x for x in list(new_suggestions_list) if ( x not in list(current_user))]
#     random.shuffle(final_suggestions_list)

#     username_profile = []
#     username_profile_list = []

#     for users in final_suggestions_list:
#         username_profile.append(users.id)

#     for ids in username_profile:
#         profile_lists = Profile.objects.filter(id_user=ids)
#         username_profile_list.append(profile_lists)

#     suggestions_username_profile_list = list(chain(*username_profile_list))


#     return render(request, 'index.html', {'user_profile': user_profile, 'posts':feed_list, 'suggestions_username_profile_list': suggestions_username_profile_list[:4]})



# def follow(request):
#     if request.method=="POST":
#         follower=request.POST['follower']
#         user=request.POST['user']

#         if FollowerCount.objects.filter(follower=follower,user=user).first():
#             delete_follower=FollowerCount.objects.get(follower=follower,user=user)
#             delete_follower.delete()
#             return redirect('/profile/'+user)
#         else:
#             new_follower=FollowerCount.objects.create(follower=follower,user=user)
#             new_follower.save()
#             return redirect('/profile/'+user)
#     else:
#         return redirect('home')
