from django .forms import ModelForm
from django import forms
from .models import *


class PostCreateForm(ModelForm):
    class Meta:
       model = Post
       fields = ['url','body', 'tags']  # Added 'media' field
       labels = {
           'body': 'Caption',
           'tags': 'Category',
       }
       widgets = {
           'body': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Add a Caption...', 'class': 'font1 text-3xl'}),
           'url': forms.TextInput(attrs={'placeholder': 'Add URLs...'}),
           'tags': forms.CheckboxSelectMultiple(),
       }
    


class PostEditForm(ModelForm):
    class Meta:
        model = Post  # Ensure the Post model has a 'body' field
        fields = ['body','tags']  # Only allow editing the 'body'
        labels = {
            'body':'',  # Hide label
            'tags':'Catagory',
        }
        widgets = {
            'body': forms.Textarea(attrs={'rows': 3, 'class': 'font1 text-3xl'}),  # Custom styling
            'tags':forms.CheckboxSelectMultiple(),
        }    
        
class CommentCreateForm(ModelForm):
    class Meta:
        model=Comment
        fields=['body']
     
        widgets = {
            'body':forms.TextInput(attrs={'placeholder': 'Add Comments..'})
        }
        labels = {
           'body':''
        }
        
class ReplyCreateForm(ModelForm):
    class Meta:
        model=Reply
        fields=['body']
        widget={
            'body':forms.TextInput(attrs={'placeholder':'Add Reply..','class':"!text-sm"})
        }
        labels = {
            'body':''
        }