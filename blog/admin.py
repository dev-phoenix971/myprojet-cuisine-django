from django.contrib import admin
from django.db import models
from tinymce.widgets import TinyMCE
from .forms import BlogForm

from .models import Blog, Likes, BlogComment


class BlogAdmin(admin.ModelAdmin):
    form = BlogForm
    list_display = ("blog_title", "blog_content", "blog_image", "publish_date", "update_date", "published")
    prepopulated_fields = {"slug": ("blog_title",)}

    formfield_overrides = {
        models.TextField: {"widget": TinyMCE()},
    }


admin.site.register(Blog, BlogAdmin)


admin.site.register(BlogComment)
admin.site.register(Likes)