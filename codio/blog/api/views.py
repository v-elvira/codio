from rest_framework import generics

from blog.api.serializers import PostSerializer, UserSerializer, PostDetailSerializer, TagSerializer
from blog.models import Post, Tag

# from rest_framework.authentication import TokenAuthentication #SessionAuthentication
from rest_framework.permissions import IsAdminUser
from blog.api.permissions import AuthorModifyOrReadOnly, IsAdminUserForObject

from codio_auth.models import User

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

# for caching:
# NOTE: DRF GUI based responses aren’t cached (?? OK in my DRF version). Use Postman
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers, vary_on_cookie

from rest_framework.exceptions import PermissionDenied

# from rest_framework.throttling import ScopedRateThrottle

from django.db.models import Q
from django.utils import timezone
from datetime import timedelta
from django.http import Http404

# from rest_framework.pagination import PageNumberPagination
# import django_filters.rest_framework # if want to set filter_backends here (instead of settings.py)
from blog.api.filters import PostFilterSet
# # VeiwSets, ModelViewSets:

# class TagViewSet(viewsets.ViewSet):
#     def list(self, request):
#         queryset = Tag.objects.all()
#         serializer = TagSerializer(queryset, many=True)
#         return Response(serializer.data) # rest_framework.response.Response

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    # to select posts with a selected tag:
    # generated path will be /api/v1/tags/<pk>/posts/ (the name of the method being appended to the detail URL for a Tag). 
    # path can be set in url_path parameter; url_name in url_name (default tag-posts); in name - name in GUI Extra Actions menu
    @action(methods=["get"], detail=True, name="Posts with the Tag")  # @action => URL would be set up
    def posts(self, request, pk=None):
        tag = self.get_object()  # ModelViewSet.get_object() helper method to fetch by pk

        # page = self.paginate_queryset(tag.posts) # TypeError: 'ManyRelatedManager' object is not subscriptable
        page = self.paginate_queryset(tag.posts.all())
        if page is not None:
            post_serializer = PostSerializer(
                page, many=True, context={"request": request}
            )
            return self.get_paginated_response(post_serializer.data)

        post_serializer = PostSerializer(
            tag.posts, many=True, context={"request": request} # request is used there in HyperlinkRelatedField creation
        )
        return Response(post_serializer.data)

    @method_decorator(cache_page(2)) # in seconds. Don't like it, so set small (300 was, 5 min)
    def list(self, *args, **kwargs):
        return super(TagViewSet, self).list(*args, **kwargs)

    @method_decorator(cache_page(2))
    def retrieve(self, *args, **kwargs):
        return super(TagViewSet, self).retrieve(*args, **kwargs)


class PostViewSet(viewsets.ModelViewSet):
    # filter_backends = [django_filters.rest_framework.DjangoFilterBackend] # or globally in settings.py
    filterset_fields = ["author", "tags"] # "author__email" ok (model field, equality). "published_at__gte" needs filterset_class
    filterset_class = PostFilterSet       # if use custom filter settings, subclassing FilterSet
    ordering_fields = ["published_at", "author", "title", "slug"]

    # pagination_class = PageNumberPagination # page_size from settings.py PAGE_SIZE (default None) or override in subclass

    # throttle_classes = [ScopedRateThrottle] # rest_framework.throttling 
    # throttle_scope = "post_api"             # settings.py

    permission_classes = [AuthorModifyOrReadOnly | IsAdminUserForObject]
    queryset = Post.objects.all()

    def get_queryset(self):
        # self.request.query_params to access and use in filtering (?param=week) instead of /week/

        if self.request.user.is_anonymous:
            # published only
            queryset = self.queryset.filter(published_at__lte=timezone.now())

        elif self.request.user.is_staff:
            # allow all
            queryset = self.queryset
        else:
            queryset = self.queryset.filter(
                Q(published_at__lte=timezone.now()) | Q(author=self.request.user)
            )

        time_period_name = self.kwargs.get("period_name")

        if not time_period_name:
            # no further filtering required
            return queryset

        if time_period_name == "new":
            return queryset.filter(
                published_at__gte=timezone.now() - timedelta(hours=1)
            )
        elif time_period_name == "today":
            return queryset.filter(
                published_at__date=timezone.now().date(),
            )
        elif time_period_name == "week":
            return queryset.filter(published_at__gte=timezone.now() - timedelta(days=7))
        else:
            raise Http404(
                f"Time period {time_period_name} is not valid, should be "
                f"'new', 'today' or 'week'"
            )

    def get_serializer_class(self):
        if self.action in ("list", "create"):
            return PostSerializer
        return PostDetailSerializer

    @method_decorator(cache_page(2))
    @method_decorator(vary_on_headers("Authorization"))
    @method_decorator(vary_on_cookie)
    # @method_decorator(vary_on_headers("Authorization", "Cookie")) # shorter version of the last two
    @action(methods=["get"], detail=False, name="Posts by the logged in user")
    def mine(self, request):
        if request.user.is_anonymous:
            raise PermissionDenied("You must be logged in to see which Posts are yours")
        posts = self.get_queryset().filter(author=request.user)

        page = self.paginate_queryset(posts)
        if page is not None:
            serializer = PostSerializer(page, many=True, context={"request": request})
            return self.get_paginated_response(serializer.data)

        serializer = PostSerializer(posts, many=True, context={"request": request}) # if pagination is turned off in settings => page=None => ordinary response
        return Response(serializer.data)

    @method_decorator(cache_page(1))
    def list(self, *args, **kwargs):
        return super(PostViewSet, self).list(*args, **kwargs)


# end ViewSets

# class PostList(generics.ListCreateAPIView): # replaced by PostViewSet
#     # authentication_classes = [TokenAuthentication]
#     # permission_classes = [IsAdminUser]
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer

#     ## check for logging: request.user.is_anonymous (!) or ...is_authenticated
#     ## User is not None, is_anonymous not shown in __dict__ (django.utils.functional.SimpleLazyObject: User or AnonymousUser)
    
#     # def get(self, request, *args, **kwargs):
#     #     print(request.user, request.user is None, type(request.user), "anon: ", request.user.is_anonymous, "auth: ", request.user.is_authenticated) 
#     #     #request.user.email => error for anonymous
#     #     return super().get(request, *args, **kwargs)


# class PostDetail(generics.RetrieveUpdateDestroyAPIView):   # replaced by PostViewSet
#     permission_classes = [AuthorModifyOrReadOnly | IsAdminUserForObject] # after adding comment-adding through API they are also forbidden for not author | admins
#     queryset = Post.objects.all()
#     # serializer_class = PostSerializer
#     serializer_class = PostDetailSerializer


class UserDetail(generics.RetrieveAPIView):
    lookup_field = "email"
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # @method_decorator(cache_page(300))
    # def get(self, *args, **kwargs):
    #     return super(UserDetail, self).get(*args, *kwargs)


# from rest_framework import mixins
# from rest_framework import generics
# from blog.models import Post
# from blog.api.serializers import PostSerializer


# class PostList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)


# class PostDetail(
#     mixins.RetrieveModelMixin,
#     mixins.UpdateModelMixin,
#     mixins.DestroyModelMixin,
#     generics.GenericAPIView,
# ):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer

#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)

#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)

#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)
