from django.shortcuts import get_object_or_404, redirect, render

from blogs.models import Category, Blog, About
from .forms import RegistrationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import auth

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


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            print(form.errors)
    else:
        form = RegistrationForm()
    context = {
        'form':form
    }
    return render(request, 'register.html', context)

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            print(username)
            print(password)
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                print('user is found :: '+str(user))
                auth.login(request, user)
            return redirect('dashboard')
        else:
            print(form.errors)
    else:
        form = AuthenticationForm()
    context = {
        'form':form
    }
    return render(request, 'login.html', context)


def logout(request):
    auth.logout(request)
    return redirect('home')