from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, DetailView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import blog_post

# Create your views here.
class Index(ListView):
    model = blog_post
    queryset = blog_post.objects.all().order_by('-date')
    template_name = 'index.html'
    paginate_by = 1

class Featured(ListView):
    model = blog_post
    queryset = blog_post.objects.filter(featured = True).order_by('-date')
    template_name = 'featured.html'
    paginate_by = 1 

class DetailFeaturedArticleView(DetailView):
    model = blog_post                           
    template_name='featured_blog_post.html'

    def get_context_data(self, *args, **kwargs):
        context= super(DetailFeaturedArticleView, self).get_context_data(*args, **kwargs)
        article = blog_post.objects.get(id=self.kwargs.get('pk'))
        context['liked_by_user'] = False

        if article.likes.filter(pk=self.request.user.id).exists():
            context['liked_by_user'] = True
            
        return context 
    
class DetailArticleView(DetailView):
    model = blog_post                           
    template_name='blog_post.html'

    def get_context_data(self, *args, **kwargs):
        context= super(DetailArticleView, self).get_context_data(*args, **kwargs)
        article = blog_post.objects.get(id=self.kwargs.get('pk'))
        context['liked_by_user'] = False

        if article.likes.filter(pk=self.request.user.id).exists():
            context['liked_by_user'] = True
            
        return context 


class LikeArticle(View):
    def post(self, request, pk):
        article = blog_post.objects.get(id=pk)
        if article.likes.filter(pk=self.request.user.id).exists():
            article.likes.remove(request.user.id)
        else:
            article.likes.add(request.user.id)

        article.save()
        return redirect('detail_article', pk)
    

class DeleteArticleView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = blog_post
    template_name = 'delete.html'
    success_url = reverse_lazy('index')

    def test_func(self):
        article = blog_post.objects.get(id=self.kwargs.get('pk'))
        return self.request.user.id == article.auhtor.id