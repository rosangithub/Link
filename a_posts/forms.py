from django .forms import ModelForm
from django import forms
from .models import *


class PostCreateForm(ModelForm):
    class Meta:
       model =Post
       fields=['url','body','tags']
       labels={
           'body':'Caption',
           'tags':'Category',
       }
       widgets={
           'body': forms.Textarea(attrs={'rows':3,'placeholder':'Add a Caption...','class':'font1 text-3xl'}),
           'url':forms.TextInput(attrs={'placeholder':'Add urls...'}),
           'tags':forms.CheckboxSelectMultiple(),
       }



class PostEditForm(ModelForm):
    class Meta:
        model = Post  # Ensure the Post model has a 'body' field
        fields = ['body','tags']  # Only allow editing the 'body'
        labels = {
            'body': '',  # Hide label
            'tags':'Catagory',
        }
        widgets = {
            'body': forms.Textarea(attrs={'rows': 3, 'class': 'font1 text-3xl'}),  # Custom styling
            'tags':forms.CheckboxSelectMultiple(),
        }    