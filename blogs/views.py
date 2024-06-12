from django.shortcuts import get_object_or_404, render

from django.http import HttpResponse, HttpResponseRedirect
from .models import Category, Blog, Comment
from django.db.models import Q


def post_by_category(request, category_id):
    # fetch the posts that belongs to the category with the id category_id
    posts = Blog.objects.filter(status='published', category=category_id)
    category = get_object_or_404(Category, pk=category_id)
    context = {
        'posts':posts,
        'category':category,
    }
    return render(request, 'post_by_category.html', context)


def blogs(request, slug):
    single_blog = get_object_or_404(Blog, slug=slug, status='published')
    if request.method == 'POST':
        # # 1st way
        # try:
        #     Comment.objects.create(comment=request.POST['comment'], user=request.user, blog=single_blog)
        # except:
        #     print('Error occured while creating comment in the DB.')

        # 2nd way
        comment = Comment()
        comment.user = request.user
        comment.blog = single_blog
        comment.comment = request.POST['comment']
        comment.save()
        return HttpResponseRedirect(request.path_info)

    comments = Comment.objects.filter(blog=single_blog)
    comments_count = comments.count()
    context = {
        'single_blog':single_blog,
        'comments':comments,
        'comments_count':comments_count
    }
    return render(request, 'blogs.html', context)


def search(request):
    keyword = request.GET.get('keyword') # dict get method
    blogs = Blog.objects.filter(Q(title__icontains=keyword) | Q(short_description__icontains=keyword) | Q(blog_body__icontains=keyword), status='published')
    context = {
        'blogs':blogs,
        'keyword':keyword,
    }
    return render(request, 'search.html', context)