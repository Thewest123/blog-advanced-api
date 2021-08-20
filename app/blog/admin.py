from django.contrib import admin
from django.utils.translation import ugettext as _
from django.template.defaultfilters import truncatewords
from blog import models


class TagAndCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ['name']}
    search_fields = ['name', 'slug']
    list_display = ['name', 'slug']
    ordering = ['name']


class CommentAdmin(admin.ModelAdmin):
    list_display = ['short_content', 'author', 'blog_post', 'creation_date']
    search_fields = ['blog_post', 'author', 'content']
    date_hierarchy = 'creation_date'

    def short_content(self, obj):
        return truncatewords(obj.content, 15)


class CommentInline(admin.TabularInline):
    model = models.Comment
    fk_name = 'blog_post'
    extra = 0


class BlogPostAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ['title']}
    search_fields = ['title', 'slug']
    list_filter = ['category', 'tags', 'author']
    list_display = ['title', 'category', 'author']
    date_hierarchy = 'creation_date'
    fieldsets = (
        (_('Blog post details'), {
            'fields': ['title', 'slug', 'author',
                       'category', 'tags', 'content']
        }),
        (_('Miscellaneous'), {
            'fields': ['creation_date']
        }),
    )
    inlines = [CommentInline]


admin.site.register(models.Tag, TagAndCategoryAdmin)
admin.site.register(models.Category, TagAndCategoryAdmin)
admin.site.register(models.Comment, CommentAdmin)
admin.site.register(models.BlogPost, BlogPostAdmin)

# Display '(None)' insted of '-' for null values
admin.site.empty_value_display = '(None)'
