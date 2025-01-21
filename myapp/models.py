from django.db import models
from tinymce.models import HTMLField
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.

class blog_post(models.Model):
    title = models.CharField(max_length=255)
    header_image = models.ImageField(null=True, blank=True, upload_to="images/")
    content = RichTextField(blank= True, null=True)
    date = models.DateField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    featured = models.BooleanField(default=False)
    likes = models.ManyToManyField(User, related_name='likes', blank=True)
    category = models.CharField(max_length=255, default='random')

    def get_absolute_url(self):
        return reverse('detail_article', kwargs={'pk': self.pk})
    
class category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('detail_article', kwargs={'pk': self.pk})
    

class comment(models.Model):
    post = models.ForeignKey(blog_post,related_name="comments" ,on_delete = models.CASCADE)
    name = models.CharField(max_length=255)
    body = models.TextField()
    date = models.DateField(auto_now_add=True)

    def __str__ (self):
        return '%s - %s' % (self.post.title, self.name)

