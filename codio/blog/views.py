from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from blog.models import Post

from django.shortcuts import redirect
from blog.forms import CommentForm

import logging
from django.views.decorators.cache import cache_page
# from django.views.decorators.vary import vary_on_headers
from django.views.decorators.vary import vary_on_cookie

logger = logging.getLogger(__name__)

@cache_page(60)
# @vary_on_headers("Cookie") # the same as:
@vary_on_cookie
def index(request):
    # from django.http import HttpResponse
    # return HttpResponse((str(request.user)+str(timezone.localtime(timezone.now()))).encode("ascii"))
    posts = Post.objects.filter(published_at__lte=timezone.now()).order_by('-published_at').select_related("author")\
               # .only("title", "summary", "content", "author", "published_at", "slug") #.defer("created_at", "modified_at")
    logger.debug("Got %d posts", len(posts))
    return render(request, "blog/index.html", {"posts": posts})

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.user.is_active:
        if request.method == "POST":
            comment_form = CommentForm(request.POST)

            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.content_object = post
                comment.creator = request.user
                comment.save()
                logger.info("Created comment on Post %d for user %s", post.pk, request.user)
                return redirect(request.path_info)
        else:
            comment_form = CommentForm()
    else:
        comment_form = None
    return render(request, "blog/post-detail.html", {"post": post, "comment_form": comment_form})

def get_ip(request):
  from django.http import HttpResponse
  return HttpResponse(request.META['REMOTE_ADDR'])

# def logs(request):
#     import logging

#     logger = logging.getLogger(__name__) # default level is WARNING (and harder)

#     logger.debug("This is a debug message")
#     logger.info("This is an info message")
#     logger.warning("This is a warning message")
#     logger.error("This is an error message")
#     logger.critical("This is a critical message")
#     try:
#         1/0
#     except:
#         logger.exception("An exception occured")
#     logger.log(logging.WARNING, "Current user is %s with email %s", request.user.username, getattr(request.user, "email", '--'))
#     return render(request, "blog/index.html", {"posts": ""})
