from django.shortcuts import get_object_or_404, redirect, render
from blogs.models import Category, Blog
from django.contrib.auth.decorators import login_required
from .forms import CategoryForm, BlogPostForm, AddUserForm, EditUserForm
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User, Permission


@login_required(login_url='login')
def dashboard(request):
    category_count = Category.objects.all().count()
    blogs_count = Blog.objects.all().count()
    context = {
        'category_count':category_count,
        'blogs_count':blogs_count,
    }
    return render(request, 'dashboard/dashboard.html', context)


def categories(request):
    return render(request, 'dashboard/categories.html')


def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('categories')
    else:
        form = CategoryForm()
    context = {
        'form':form
    }
    return render(request, 'dashboard/add_category.html', context)


def edit_category(request, pk):
    category = get_object_or_404(Category, id=pk)
    if request.method == 'POST':
        if 'submit' in request.POST:
            form = CategoryForm(request.POST, instance=category)
            if form.is_valid():
                form.save()
                return redirect('categories')
        else:
            return redirect('categories')
    else:
        form = CategoryForm(instance=category)
    length = len(form.initial['category_name'])
    form.fields['category_name'].widget.attrs['onfocus'] = f'this.setSelectionRange({0}, {length})'
    context = {
        'form':form,
        'category':category
    }
    return render(request, 'dashboard/edit_category.html', context)

def delete_category(request, pk):
    # 2nd method
    category = get_object_or_404(Category, pk=pk)
    context = {
        'category':category
    }
    if request.method == 'POST':
        if 'yes' in request.POST:
            category.delete()
        return redirect('categories')
            
    return render(request, 'dashboard/delete_category.html', context)

    # 1st method

    # category = get_object_or_404(Category, pk=pk)
    # category.delete()
    # return redirect('categories')


def posts(request):
    posts = Blog.objects.all().order_by('-updated_at')
    context = {
        'posts':posts
    }
    return render(request, 'dashboard/posts.html', context)


def add_post(request):
    form = BlogPostForm()
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False) # temporarily saving the form.
            # post is a Blog model object here
            post.author_id = request.user.id
            # post.slug = slugify(post.title)
            post.save()
            # title = form.cleaned_data['title']
            # post.slug = slugify(title) + "-" + str(post.id)
            post.slug = slugify(post.title) + "-" + str(post.id)
            post.save()
            return redirect('posts')
        else:
            print('form is invalid')
            print(form.errors)
    context = {
        'form':form
    }
    return render(request, 'dashboard/add_post.html', context)


def edit_post(request, pk):
    post = get_object_or_404(Blog, pk=pk)
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save()
            title = form.cleaned_data['title']
            post.slug = slugify(title) + '-' + str(post.id)
            post.save()
            return redirect('posts')
    else:
        form = BlogPostForm(instance=post)
    context = {
        'form':form,
        'post':post
    }
    return render(request, 'dashboard/edit_post.html', context)


def delete_post(request, pk):
    post = get_object_or_404(Blog, pk=pk)
    post.delete()
    return redirect('posts')


def users(request):
    users = User.objects.all()
    permissions = get_user_permissions(request.user)
    print(permissions)
    context = {
        'users':users
    }
    return render(request, 'dashboard/users.html', context)


def add_user(request):
    form = AddUserForm()
    if request.method == 'POST':
        form = AddUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('users')
        else:
            print(form.errors)
    context = {
        'form':form
    }
    return render(request, 'dashboard/add_user.html', context)


def edit_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    form = EditUserForm(instance=user)
    if request.method =='POST':
        form = EditUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('users')
        else:
            print(form.errors)
    context = {
        'form':form,
        'user':user
    }
    return render(request, 'dashboard/edit_user.html', context)


def delete_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    user.delete()
    return redirect('users')


# Method to view permissions
def get_user_permissions(user):
    if user.is_superuser:
        return Permission.objects.all()
    return user.user_permissions.all() | Permission.objects.filter(group__user=user)
