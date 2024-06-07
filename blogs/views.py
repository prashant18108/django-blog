from django.shortcuts import get_object_or_404, render

from django.http import HttpResponse
from .models import Category, Blog


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
    context = {
        'single_blog':single_blog,
    }
    return render(request, 'blogs.html', context)