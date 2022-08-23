from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from taggit.managers import TaggableManager
# Create your models here.

class PublishManager(models.Manager):
    def get_queryset(self):
        return super(PublishManager, self).get_queryset().filter(status='published') #filtert based on published blogs


class Post(models.Model):
    STATUS=(
        ('draft','DRAFT'),
        ('published','PUBLISHED')
    )
    author=models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    title=models.CharField(max_length=220)
    slug=models.SlugField(max_length=250, unique_for_date='publish')
    body=models.TextField()
    publish=models.DateTimeField(default=timezone.now)
    created_at=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    status=models.CharField(max_length=15,choices=STATUS,default='draft')
    objects=models.Manager()
    published=PublishManager()

    def get_absolute_url(self):
        return reverse("blog:blog_details", args=[self.publish.year, self.publish.month, self.publish.day, self.slug])
    

    class Meta:  
        ordering=('-publish',) #order based on  asc & desc(defaul asc, first object) by - (desc, last object)

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name="comments")
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254,null=True,blank=True)
    body = models.TextField()
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateField(auto_now=True)
    active = models.BooleanField(default=True)
    tags = TaggableManager()

    class Meta:
        ordering = ('created',)
    
    def __str__(self):
        return f'commnt by {self.name} on {self.post}'
