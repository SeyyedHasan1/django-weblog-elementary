from django.urls import path
from . import views

app_name='blog'

urlpatterns = [
    path("", views.blog_list, name='blog_list'),
    path("<int:year>/<int:month>/<int:day>/<slug:post>/", views.blog_details, name='blog_details'),
    path("<int:pk>/share/", views.share_post, name='share_post')
]
