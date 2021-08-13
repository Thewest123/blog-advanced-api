from django.contrib.auth import get_user_model
from rest_framework import viewsets, mixins

from blog.models import BlogPost, Category, Tag, Comment
from blog import serializers


class BlogPostViewSet(viewsets.ModelViewSet):

    queryset = BlogPost.objects.all()
    lookup_field = 'slug'

    serializer_classes = {
        'default': serializers.BlogPostSerializer,
        'create': serializers.BlogPostCreateUpdateSerializer,
        'update': serializers.BlogPostCreateUpdateSerializer,
        'retrieve': serializers.BlogPostDetailSerializer,
    }

    def get_serializer_class(self):
        """Set different serializer class for different actions"""
        if self.action == 'retrieve':
            return self.serializer_classes.get('retrieve')
        elif self.action == 'create':
            return self.serializer_classes.get('create')
        elif self.action == 'update':
            return self.serializer_classes.get('update')
        else:
            return self.serializer_classes.get('default')

    def get_queryset(self):
        """Filter the results based on query parameters"""
        queryset = self.queryset

        # Get query params and filter the queryset
        author = self.request.query_params.get('author')
        category = self.request.query_params.get('category')
        tags = self.request.query_params.get('tags')

        if author:
            queryset = queryset.filter(author__id__exact=int(author))

        if category:
            queryset = queryset.filter(category__slug__exact=category)

        if tags:
            tags_list = tags.split(',')
            queryset = queryset.filter(tags__slug__in=tags_list).distinct()

        return queryset.order_by('-creation_date')


class TagViewSet(viewsets.ModelViewSet):

    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer


class CategoryViewSet(viewsets.ModelViewSet):

    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer


class CommentViewSet(viewsets.GenericViewSet,
                     mixins.RetrieveModelMixin,
                     mixins.CreateModelMixin,
                     mixins.DestroyModelMixin,
                     ):
    """
    ViewSet for the Comment model,
    only instance GET, POST and DELETE allowed
    """

    queryset = Comment.objects.all()

    serializer_classes = {
        'default': serializers.CommentSerializer,
        'create': serializers.CommentCreateSerializer,
    }

    def get_serializer_class(self):
        """Set different serializer class for different actions"""
        if self.action == 'create':
            return self.serializer_classes.get('create')
        else:
            return self.serializer_classes.get('default')


class UserViewSet(viewsets.ModelViewSet):

    queryset = get_user_model().objects.all()
    serializer_class = serializers.UserSerializer
