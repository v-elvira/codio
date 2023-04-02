from django import template
from django.contrib.auth.models import User

from django.utils.html import escape
from django.utils.safestring import mark_safe

from django.utils.html import format_html
from blog.models import Post
from django.utils import timezone

register = template.Library()

@register.filter
def author_details(author, current_user=None):
	if not isinstance(author, User):
		return ''

	if author == current_user:
		return format_html("<strong>me</strong>")

	if author.first_name and author.last_name:
		# name = escape(f'{author.first_name} {author.last_name}')
		name = f"{author.first_name} {author.last_name}"
	else:
		# name = escape(f'{author.username}')
		name = f"{author.username}"

	if author.email:
		# email = escape(author.email)
		# prefix = f'<a href="mailto:{email}">'
		prefix = format_html('<a href="mailto:{}">', author.email)
		## prefix = format_html('<a href="mailto:{}">', author.email) # = escape arguments + mark_safe
		# suffix = "</a>"
		suffix = format_html("</a>")
	else:
		prefix = ""
		suffix = ""

	# return mark_safe(f"{prefix}{name}{suffix}")
	return format_html('{}{}{}', prefix, name, suffix)


@register.simple_tag
def row(extra_classes=""):
    return format_html('<div class="row {}">', extra_classes)


@register.simple_tag
def endrow():
    return format_html("</div>")

@register.inclusion_tag("blog/post-list.html")
def recent_posts(post):
	posts = Post.objects.filter(published_at__lte=timezone.now()).exclude(pk=post.pk).order_by('-published_at')[:5]
	return {"title": "Recent Posts", "posts": posts}

# @register.simple_tag # (?) parameter works fine (pdf says no)
# def recent_posts(post):
# 	posts = Post.objects.filter(published_at__lte=timezone.now()).exclude(pk=post.pk).order_by('-published_at')[:5]
# 	return format_html("<p>{}</p>", posts)


@register.simple_tag
def col(extra_classes=""):
    return format_html('<div class="col {}">', extra_classes)


@register.simple_tag
def endcol():
    return format_html("</div>")


## <small>By {% author_details_tag %} on {{ post.published_at|date:"M, d Y" }}</small>

# @register.simple_tag(takes_context=True)
# def author_details_tag(context):
#     request = context["request"]
#     current_user = request.user
#     post = context["post"]
#     author = post.author

#     if author == current_user:
#         return format_html("<strong>me</strong>")

#     if author.first_name and author.last_name:
#         name = f"{author.first_name} {author.last_name}"
#     else:
#         name = f"{author.username}"

#     if author.email:
#         prefix = format_html('<a href="mailto:{}">', author.email)
#         suffix = format_html("</a>")
#     else:
#         prefix = ""
#         suffix = ""

#     return format_html("{}{}{}", prefix, name, suffix)

