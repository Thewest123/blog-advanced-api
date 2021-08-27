from django.contrib.auth import get_user_model
from rest_framework import serializers
from blog.models import BlogPost, Category, Tag, Comment


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'email', 'name', 'address']


class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(many=False)

    class Meta:
        model = Comment
        fields = ['author', 'blog_post', 'content']


class CommentCreateSerializer(CommentSerializer):
    author = serializers.PrimaryKeyRelatedField(
        many=False,
        queryset=get_user_model().objects.all()
    )

    class Meta:
        model = Comment
        fields = ['author', 'blog_post', 'content']


class BlogPostSerializer(serializers.ModelSerializer):
    """Default serializer for the BlogPost view, primary list action"""

    tags = serializers.SlugRelatedField(
        many=True,
        slug_field='name',
        queryset=Tag.objects.all()
    )

    category = CategorySerializer(many=False)
    author = UserSerializer(many=False)

    class Meta:
        model = BlogPost
        fields = ['title', 'slug', 'category', 'tags', 'author']


class BlogPostDetailSerializer(BlogPostSerializer):
    """Serializer for the BlogPost detail view"""

    tags = TagSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    comments_count = serializers.SerializerMethodField()
    is_users_comment_inside = serializers.SerializerMethodField(
        'check_user_comment')

    def get_comments_count(self, obj) -> int:
        """Returns the comments count"""
        return obj.comments.count()

    def check_user_comment(self, obj) -> bool:
        """
        Returns true if the currently authenticated user
        has a comment inside the blog post
        """
        request = self.context.get('request', None)
        return obj.comments.filter(author__exact=request.user).exists()

    class Meta:
        model = BlogPost
        fields = '__all__'
        lookup_field = 'slug'


class BlogPostCreateUpdateSerializer(BlogPostSerializer):
    """Serializer for the BlogPost create and update view"""

    tags = serializers.SlugRelatedField(
        many=True,
        slug_field='slug',
        queryset=Tag.objects.all()
    )

    category = serializers.SlugRelatedField(
        many=False,
        slug_field='slug',
        queryset=Category.objects.all()
    )

    author = serializers.PrimaryKeyRelatedField(
        many=False,
        queryset=get_user_model().objects.all()
    )

    class Meta:
        model = BlogPost
        fields = '__all__'
        lookup_field = 'slug'
