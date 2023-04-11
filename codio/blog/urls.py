from django.urls import path
import blog.views

from django.views.generic import TemplateView

urlpatterns = [
    path("", blog.views.index),
    # path("logs", blog.views.logs),
    path("post/<slug>/", blog.views.post_detail, name="blog-post-detail"),
    path("bootstr",  TemplateView.as_view(template_name='bootstr.html')),
]