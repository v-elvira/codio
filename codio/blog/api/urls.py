from django.urls import path, include, re_path
from rest_framework.urlpatterns import format_suffix_patterns

from blog.api.views import UserDetail, TagViewSet, PostViewSet #, PostList, PostDetail
from rest_framework.authtoken import views

from drf_yasg import openapi
from drf_yasg.views import get_schema_view
# import os

from rest_framework.routers import DefaultRouter

# Settings for drf_yasg swagger generator
schema_view = get_schema_view(
    openapi.Info(
        title="Codio Blog API",
        default_version="v1",
        description="API for Codio Blog",
    ),
    # url=f"https://{os.environ.get('HOSTNAME')}/api/v1/",
    public=True,
)


# ViewSets withot Routing:
# tag_list = TagViewSet.as_view({
#     "get": "list",
#     "post": "create"
# })

# tag_detail = TagViewSet.as_view({
#     "get": "retrieve",
#     "put": "update",
#     "patch": "partial_update",
#     "delete": "destroy"
# })

# with Routing:
router = DefaultRouter()
router.register("tags", TagViewSet) # "tags" will be used as initial component of the path. Can register other prefixes
router.register("posts", PostViewSet) #, basename = api_post (_detail, how to - _ ?) Or views names will be post-detail, post-list,...

urlpatterns = [
    # path("", include(router.urls)), # error with format_suffix_patterns. DefaultRouter provides format routes (.json) by its own

    # path("posts/", PostList.as_view(), name="api_post_list"),             # replaced with router
    # path("posts/<int:pk>", PostDetail.as_view(), name="api_post_detail"), # replaced with router
    path("auth/", include("rest_framework.urls")),
    path("token-auth/", views.obtain_auth_token),
    path("users/<str:email>", UserDetail.as_view(), name="api_user_detail"),
    # re_path(                                            # url pattern with regular expressions
    #     r"^swagger(?P<format>\.json|\.yaml)$",
    #     schema_view.without_ui(cache_timeout=0),
    #     name="schema-json",
    # ),
    # path(
    #     "swagger/",
    #     schema_view.with_ui("swagger", cache_timeout=0),
    #     name="schema-swagger-ui",
    # ),
    
    # path("tags/", tag_list, name="tag_list"),
    # path("tags/<int:pk>/", tag_detail, name="tag_detail"),
]

urlpatterns = format_suffix_patterns(urlpatterns) # causes error after swagger re_path and .json not found after swagger path


urlpatterns.extend([
    re_path(                                            # url pattern with regular expressions
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("", include(router.urls)),
    path(
        "posts/by-time/<str:period_name>/",       # "posts/<int:pk>/by-time/<str:period_name>/",
        PostViewSet.as_view({"get": "list"}),     # PostViewSet.as_view({"get": "retrieve"}),
        name="posts-by-time",
    ),
    ])
