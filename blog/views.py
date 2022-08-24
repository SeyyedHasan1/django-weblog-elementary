from multiprocessing import context
from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.db.models import Count
from django.contrib.postgres.search import SearchVector , SearchQuery , SearchRank
from .forms import EmailPostForm , CommentForm , SerachForm
# Create your views here.

def blog_list(request):
    posts=Post.published.all()
    paginator=Paginator(posts,2) #4 posts per a page
    page=request.GET.get('page')
    try:
        posts=paginator.page(page)

    except PageNotAnInteger:
        posts=paginator.page(1)
    except EmptyPage:
        posts=paginator.page(paginator.num_pages)

    context={
        "posts" : posts,
        "page":page
    }
    return render(request, 'blog/blog_list.html', context)


def blog_details(request,year, month, day, post):
    post=get_object_or_404(Post,slug=post, status='published', publish__year=year, publish__month=month, publish__day=day)
    comments = post.comments.filter(active=True)
    
    post_tags_ids = post.tags.values_list('id',flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags = Count('tags')).order_by('-same_tags','-publish')
    
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
            return HttpResponseRedirect(request.path_info)
    else:
        comment_form = CommentForm()
    context = {"post":post,
        'form':comment_form,
        "comments":comments,
        "s_posts":similar_posts
    }
    return render(request,'blog/blog_details.html',context)



def share_post(request, pk):
    post=get_object_or_404(Post, id=pk, status='published')
    
    if request.method=="POST":
        form=EmailPostForm(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            post_url = request.build_absolute_uri(
                post.get_absolute_url())
            subject = f"{cd['name']} recommend you"
            message = f"{post.title} in {post_url} and {cd['comment']}"
            send_mail(
                subject,message,"admin@gmail.com",
                [cd['to']]
            )
    
    else:
        form=EmailPostForm()
    
    context={
        "post":post,
        "form":form,
    }
    return render(request, 'blog/share_post.html', context)


def post_serach(request):
    form = SerachForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SerachForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']

            # A B C D => 1.0 , 0.4 , 0.2 , 0.1
            search_vector = SearchVector('title', weight='A') + SearchVector('body' , weight="C")
            serach_query = SearchQuery(query)
            results = Post.published.annotate(search=search_vector,rank=SearchRank(search_vector, serach_query)).filter(rank__gte=0.5).order_by('-rank')
    return render(request, 'blog/post/search.html',{'form':form,'query':query,'results':results})