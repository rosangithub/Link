from django.shortcuts import render,redirect,get_object_or_404
from .forms import *

from bs4 import BeautifulSoup
import requests
from django.contrib import messages

# Create your views here.
def home_view(request,tag=None):
    if tag:
         posts=Post.objects.filter(tags__slug=tag)
         tag=get_object_or_404(Tag,slug=tag)
    else:
        posts=Post.objects.all()#retrieve all the objects from the Post
    catagories=Tag.objects.all()
    context={
        'posts':posts,
        'catagories':catagories,
        'tag':tag,
    }
    return render(request, 'a_posts/home.html',context )

# def catagory_view(request,tag):
#     posts=Post.objects.filter(tags__slug=tag)
#     return render(request,'a_posts/home.html',{'posts': posts})

# def hom_view(request):
#     posts=Post.objects.all()#retrieve all the objects from the Post
#     return render(request, 'a_posts/home.html',{'posts':posts })

def post_create_view(request):
    form =PostCreateForm()#create an empty form instance
    if request.method=="POST":
        form=PostCreateForm(request.POST)# Bind submitted data to the form
        if form.is_valid():
            post=form.save(commit=False)
            
            website=requests.get(form.data['url'])# to establish the connection with the website  url
            
            sourcecode=BeautifulSoup(website.text,'html.parser') # Parse the HTML content
            
            find_image=sourcecode.select('meta[content^="https://live.staticflickr.com/"]')
            
            image=find_image[0]['content']
            post.image=image
            
            find_title=sourcecode.select('h1.photo-title')
            title=find_title[0].text.strip()
            post.title=title
            
            find_artist=sourcecode.select('a.owner-name')
            artist=find_artist[0].text.strip()
            post.artist=artist
            
            post.save()
            form.save_m2m()
            return redirect('home')
            
    return render (request, 'a_posts/post_create.html', {'form' : form})

def post_delete_view(request,pk):
    post=get_object_or_404(Post,id=pk)
    
    if request.method=="POST":
        post.delete()
        messages.success(request,'Post deleted')
        return redirect('home')
    
    
    return render(request,'a_posts/post_delete.html',{'post':post})


def post_edit_view(request,pk):
    post=get_object_or_404(Post,id=pk)
    form=PostEditForm(instance=post)
    
    if request.method=="POST":
       form=PostEditForm(request.POST,instance=post) 
       if form.is_valid():
         form.save()
         messages.success(request,'Post updated successful')
         return redirect('home')
    
    context={
        'form':form,
         'post':post
    }
    return render(request,'a_posts/post_edit.html',context)

def post_page_view(request,pk):
    # post=Post.objects.get(id=pk)
    post=get_object_or_404(Post,id=pk)
    return render(request,'a_posts/post_page.html',{'post':post})
