from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponseRedirect
from django.views import View
from django.views.generic import ListView, DetailView, DeleteView, CreateView,UpdateView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import blog_post, comment
from .forms import BlogPostForm, blogCommentForm, category
from django.db.models import Q

# Create your views here.
class Index(ListView):
    model = blog_post
    queryset = blog_post.objects.all().order_by('-date')
    template_name = 'index.html'
    paginate_by = 1

    def get_context_data(self, *args, **kwargs):
        cat_menu = category.objects.all()
        context = super(Index, self).get_context_data( *args, **kwargs)
        context["cat_menu"] = cat_menu
        return context

def CategoryView(request, cats):
    category_posts = blog_post.objects.filter(category = cats.replace('-', ' '))
    cat_menu = category.objects.all()
    return render(request, 'category.html', {
        'cats': cats.title().replace('-', ' '),
        'category_posts':category_posts,
        'cat_menu': cat_menu
    })



class Featured(ListView):
    model = blog_post
    queryset = blog_post.objects.filter(featured = True).order_by('-date')
    template_name = 'featured.html'
    paginate_by = 1 

    def get_context_data(self, *args, **kwargs):
        cat_menu = category.objects.all()
        context = super(Featured, self).get_context_data( *args, **kwargs)
        context["cat_menu"] = cat_menu
        return context

class DetailFeaturedArticleView(DetailView):
    model = blog_post
    template_name = 'featured_blog_post.html'

    def get_context_data(self, *args, **kwargs):
        context = super(DetailFeaturedArticleView, self).get_context_data(*args, **kwargs)
        
        # Add liked_by_user logic
        article = self.get_object()
        context['liked_by_user'] = False
        if self.request.user.is_authenticated and article.likes.filter(pk=self.request.user.id).exists():
            context['liked_by_user'] = True
        
        # Add category menu
        context['cat_menu'] = category.objects.all()
        
        return context

    
    
# class DetailArticleView(DetailView):
#     model = blog_post                           
#     template_name='blog_post.html'

#     def get_context_data(self, *args, **kwargs):
#         context= super(DetailArticleView, self).get_context_data(*args, **kwargs)
#         article = blog_post.objects.get(id=self.kwargs.get('pk'))
#         context['liked_by_user'] = False

#         if article.likes.filter(pk=self.request.user.id).exists():
#             context['liked_by_user'] = True
            
#         return context 

#     def get_context_data(self, *args, **kwargs):
#         cat_menu = category.objects.all()
#         context = super(DetailArticleView, self).get_context_data( *args, **kwargs)
#         context["cat_menu"] = cat_menu
#         return context

class DetailArticleView(DetailView):
    model = blog_post
    template_name = 'blog_post.html'

    def get_context_data(self, *args, **kwargs):
        context = super(DetailArticleView, self).get_context_data(*args, **kwargs)
        
        # Add liked_by_user logic
        article = self.get_object()
        context['liked_by_user'] = False
        if self.request.user.is_authenticated and article.likes.filter(pk=self.request.user.id).exists():
            context['liked_by_user'] = True
        
        # Add category menu
        context['cat_menu'] = category.objects.all()
        
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
        return self.request.user.id == article.author.id
    
class AddArticleView(CreateView):
    model = blog_post
    template_name = 'add_post.html'
    form_class = BlogPostForm
    # fields =  ['title', 'content', 'author']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class UpdateArticleView(LoginRequiredMixin, UserPassesTestMixin,UpdateView):
    model = blog_post
    template_name ='edit_post.html'
    fields = ['title', 'category', 'content', 'header_image']

    def test_func(self):
        article = blog_post.objects.get(id=self.kwargs.get('pk'))
        return self.request.user.id == article.author.id

class AddCommentView(CreateView):
    model = comment
    template_name = 'blog_post.html'
    form_class = blogCommentForm

    def form_valid(self, form):
        post_id = self.kwargs['pk']  
        post = get_object_or_404(blog_post, id=post_id)
        form.instance.post = post  
        form.instance.name = self.request.user.username  
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.post.get_absolute_url()

    # def form_valid(self, form):
    #     form.instance.author = self.request.user
    #     return super().form_valid(form)

def SearchView(request):
    if request.method == "POST":
        searched = request.POST.get('searched', '')
        blog = blog_post.objects.filter(
            Q(title__icontains = searched) |
            Q(author__username__icontains=searched))
        
        return render(request, 'search.html',
                      {'searched':searched,
                       'blog':blog
                       })
    else:
        return render(request, 'search.html',
                      {})
    
