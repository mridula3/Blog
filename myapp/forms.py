from django import forms 
from .models import blog_post,comment, category


choices = category.objects.all().values_list('name', 'name')
choice_list = []

for item in choices:
    choice_list.append(item)

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = blog_post
        fields = ['title','category','content','header_image']

        widgets = {
             'category' : forms.Select(choices = choice_list , attrs={'class': 'form-control'}),
        }

class blogCommentForm(forms.ModelForm):
    class Meta:
        model = comment
        fields = ['body']