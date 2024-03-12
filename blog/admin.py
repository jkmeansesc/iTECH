from django.contrib import admin
from .models import Blog, Comment, Subscribe


class BlogAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Blog, BlogAdmin)
admin.site.register(Comment)
admin.site.register(Subscribe)


