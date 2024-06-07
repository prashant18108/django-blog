from django.shortcuts import get_object_or_404, redirect, render
from blogs.models import Category, Blog
from django.contrib.auth.decorators import login_required
from .forms import CategoryForm


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
    form.fields['category_name'].widget.attrs['onfocus'] = f'this.setSelectionRange({length}, {length})'
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
