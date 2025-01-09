from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, DetailView
from .models import blog_post

# Create your views here.
class Index(ListView):
    model = blog_post
    queryset = blog_post.objects.all().order_by('-date')
    template_name = 'index.html'
    paginate_by = 1

class DetailArticleView(DetailView):
    model = blog_post
    template_name='blog_post.html'