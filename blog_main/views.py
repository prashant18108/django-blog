from django.shortcuts import get_object_or_404, render

from blogs.models import Category, Blog, About

def home(request):
    featured_posts = Blog.objects.filter(is_featured=True, status='published').order_by('-updated_at')
    other_posts = Blog.objects.filter(is_featured=False, status='published')
    # about = About.objects.all().order_by('-updated_at')[0]
    try:
        about = About.objects.get()
    except:
        about = None
    context = {
        'featured_posts':featured_posts,
        'other_posts':other_posts,
        'about':about
    }
    return render(request, 'home.html', context)