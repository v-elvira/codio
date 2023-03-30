from django.contrib import admin
from blog.models import Tag, Post

admin.site.register(Tag)


class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ['title', 'author', 'summary', 'created_at', 'modified_at']
    # fields = [field.name for field in Post._meta.get_fields()]



admin.site.register(Post, PostAdmin)


# @admin.register(Post)
# class PostAdmin(admin.ModelAdmin):
# 	list_display = ('slug',)
# 	prepopulated_fields = {"slug": ("title",)}
