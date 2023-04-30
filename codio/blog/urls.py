from django.urls import path, include
import blog.views

from django.views.generic import TemplateView

from django.conf import settings
import debug_toolbar

from django.conf.urls.static import static

urlpatterns = [
    path("", blog.views.index),
    # path("logs", blog.views.logs),
    path("post/<slug>/", blog.views.post_detail, name="blog-post-detail"),
    path("bootstr",  TemplateView.as_view(template_name='bootstr.html')),
    path("ip/", blog.views.get_ip),
]

if settings.DEBUG:
    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)