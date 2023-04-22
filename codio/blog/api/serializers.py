from rest_framework import serializers
from blog.models import Post, Tag
from codio_auth.models import User


class PostSerializer(serializers.ModelSerializer):
    # tags = serializers.PrimaryKeyRelatedField(read_only=True, many=True)
    # tags = serializers.StringRelatedField(many=True) # shown as string, impossible to write (POST, PUT)
    tags = serializers.SlugRelatedField(  # modifyable, error in PUT/POST if Tag.value selected is not unique 
        slug_field="value", many=True, queryset=Tag.objects.all()
        )
    author = serializers.HyperlinkedRelatedField(
        queryset=User.objects.all(), view_name="api_user_detail", lookup_field="email"
        )

    class Meta:
        model = Post
        fields = "__all__"
        readonly = ["modified_at", "created_at"]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]
