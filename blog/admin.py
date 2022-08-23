from django.contrib import admin
from .models import Post, Comment
# Register your models here.
# admin.site.register(Post)

@admin.register(Post)   #using decorator to personalise amin panel
class PostAdmin(admin.ModelAdmin):
    list_display=('title','author','slug','status','publish')
    list_filter=('status','title')  #filter based on status, title and ect.
    search_fields=('body',)       #search on body and ect.
    date_hierarchy='publish'    #filter based on publish day and ect, under search bar
    list_editable=('status',)   #editable status field with this contains


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name','email','post','created','active']
    list_filter = ('active','created','updated')
    search_fields = ('name','email','body')