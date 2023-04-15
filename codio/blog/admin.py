from django.contrib import admin
from blog.models import Tag, Post, Comment, AuthorProfile

admin.site.register(Tag)
# admin.site.register(Comment)

class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ['title', 'author', 'summary', 'created_at', 'modified_at']
    # fields = [field.name for field in Post._meta.get_fields()] #error created_at (and modified_at) is not editable


admin.site.register(Post, PostAdmin)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
	list_display = [field.name for field in Comment._meta.get_fields() if field.name not in ('id', 'creator')]
	# exclude = ["creator"]


admin.site.register(AuthorProfile)