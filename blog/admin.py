from django.contrib import admin
from .models import Blog


class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'tag', 'content', 'comment_num', 'image', 'date')
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Blog, BlogAdmin)
