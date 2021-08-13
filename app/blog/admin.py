from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import ugettext as _
from blog import models


class TagAndCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ['name']}
    search_fields = ['name', 'slug']
    list_display = ['name', 'slug']
    ordering = ['name']


class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'content']
    ordering = ['creation_date']


class BlogPostAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ['title']}
    search_fields = ['title', 'slug']
    list_filter = ['category', 'tags', 'author']
    list_display = ['title', 'category', 'author']
    date_hierarchy = 'creation_date'
    fieldsets = (
        (_('Blog post details'), {
            'fields': ['title', 'slug', 'author', 'category', 'content']
        }),
        (_('Miscellaneous'), {
            'fields': ['creation_date']
        }),
    )


admin.site.register(models.Tag, TagAndCategoryAdmin)
admin.site.register(models.Category, TagAndCategoryAdmin)
admin.site.register(models.Comment, CommentAdmin)
admin.site.register(models.BlogPost, BlogPostAdmin)
