from django.db import models
from django.conf import settings
from django.utils import timezone


# Default category for new Blog Posts, also gets
# assigned when the post's category is deleted
UNCATEGORIZED_CATEGORY_ID = 1


class BlogPost(models.Model):
    """Model for the Blog Post"""

    title = models.CharField(max_length=80)

    slug = models.SlugField(unique=True)

    category = models.ForeignKey(
        'Category',
        on_delete=models.SET_DEFAULT,
        default=UNCATEGORIZED_CATEGORY_ID)

    tags = models.ManyToManyField('Tag', blank=True)

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    content = models.TextField()

    creation_date = models.DateTimeField(
        default=timezone.now
    )

    def __str__(self) -> str:
        return self.title


class Comment(models.Model):

    blog_post = models.ForeignKey(
        'BlogPost',
        related_name='comments',
        on_delete=models.CASCADE
    )

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    content = models.TextField()

    creation_date = models.DateTimeField(
        default=timezone.now
    )

    def __str__(self):
        """Returns author and up to 20 char preview of the comment content"""
        return (
            f'{self.author} || {self.content[:20]}'
            f'{"..." if len(self.content) > 20 else ""}'
        )


class Category(models.Model):
    name = models.CharField(max_length=80)
    slug = models.SlugField(unique=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name_plural = 'categories'


class Tag(models.Model):
    name = models.CharField(max_length=80)
    slug = models.SlugField(unique=True)

    def __str__(self) -> str:
        return self.name
