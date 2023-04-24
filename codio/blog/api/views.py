from rest_framework import generics

from blog.api.serializers import PostSerializer, UserSerializer, PostDetailSerializer
from blog.models import Post

# from rest_framework.authentication import TokenAuthentication #SessionAuthentication
from rest_framework.permissions import IsAdminUser
from blog.api.permissions import AuthorModifyOrReadOnly, IsAdminUserForObject

from codio_auth.models import User


class PostList(generics.ListCreateAPIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAdminUser]
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    ## check for logging: request.user.is_anonymous (!) or ...is_authenticated
    ## User is not None, is_anonymous not shown in __dict__ (django.utils.functional.SimpleLazyObject: User or AnonymousUser)
    
    # def get(self, request, *args, **kwargs):
    #     print(request.user, request.user is None, type(request.user), "anon: ", request.user.is_anonymous, "auth: ", request.user.is_authenticated) 
    #     #request.user.email => error for anonymous
    #     return super().get(request, *args, **kwargs)


class PostDetail(generics.RetrieveUpdateDestroyAPIView): 
    permission_classes = [AuthorModifyOrReadOnly | IsAdminUserForObject] # after adding comment-adding through API they are also forbidden for not author | admins
    queryset = Post.objects.all()
    # serializer_class = PostSerializer
    serializer_class = PostDetailSerializer


class UserDetail(generics.RetrieveAPIView):
    lookup_field = "email"
    queryset = User.objects.all()
    serializer_class = UserSerializer


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
