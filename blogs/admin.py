from django.contrib import admin
from django.http import HttpRequest

from .models import Category, Blog, About, SocialLink, Comment


class BlogAdmin(admin.ModelAdmin): 
    prepopulated_fields = {'slug':('title',)}
    list_display = ('title', 'category', 'author', 'status', 'is_featured')
    search_fields = ('id', 'title', 'category__category_name', 'status')
    list_editable = ('is_featured', 'status')


class AboutAdmin(admin.ModelAdmin):
    def has_add_permission(self, request: HttpRequest) -> bool:
        count = About.objects.all().count()
        if count == 0:
            return True
        return False
    

class CommentAdmin(admin.ModelAdmin):
    list_display = ('comment', 'blog', 'user')
    search_fields = ('comment', 'blog__title', 'user__username')


admin.site.register(Category)
admin.site.register(Blog, BlogAdmin)
admin.site.register(About, AboutAdmin)
admin.site.register(SocialLink)
admin.site.register(Comment, CommentAdmin)
