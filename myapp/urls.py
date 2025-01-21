from django.urls import path, include
from . import views
from .views import Index, DetailArticleView,LikeArticle,Featured,DetailFeaturedArticleView, DeleteArticleView,AddArticleView,UpdateArticleView,AddCommentView, SearchView, CategoryView

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('tinymce/', include('tinymce.urls')),
    path('<int:pk>/', DetailArticleView.as_view(), name='detail_article'),
    path('<int:pk>/like', LikeArticle.as_view(), name='like_article'),
    path('featured/', Featured.as_view(), name='featured'),
    path('<int:pk>/featured', DetailFeaturedArticleView.as_view(), name='detail_featured_article'),
    path('<int:pk>/delete/', DeleteArticleView.as_view(), name='delete_article'),
    path('add_post/', AddArticleView.as_view(), name='add_article'),
    path('<int:pk>/edit_post/', UpdateArticleView.as_view(), name='edit_article'),
    path('<int:pk>/add_comment/', AddCommentView.as_view(), name='add_comment'),
    path('<str:cats>/category/', CategoryView, name='category'),
    path('search', views.SearchView, name='search'),

]