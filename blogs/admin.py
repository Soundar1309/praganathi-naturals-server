from django.contrib import admin
from .models import Blog, BlogCategory, BlogTag, BlogComment

@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description']

@admin.register(BlogTag)
class BlogTagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'status', 'featured', 'published_date', 'created_at']
    list_filter = ['status', 'featured', 'category', 'tags', 'created_at', 'published_date']
    search_fields = ['title', 'summary', 'content']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['tags']
    date_hierarchy = 'published_date'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'summary', 'content')
        }),
        ('Media', {
            'fields': ('thumbnail', 'hero_image')
        }),
        ('Categorization', {
            'fields': ('category', 'tags')
        }),
        ('Publishing', {
            'fields': ('status', 'featured', 'published_date')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not change:  # Creating new blog
            obj.author = request.user
        super().save_model(request, obj, form, change)

@admin.register(BlogComment)
class BlogCommentAdmin(admin.ModelAdmin):
    list_display = ['author_name', 'blog', 'created_at', 'approved']
    list_filter = ['approved', 'created_at']
    search_fields = ['author_name', 'author_email', 'content']
    actions = ['approve_comments', 'disapprove_comments']
    
    def approve_comments(self, request, queryset):
        queryset.update(approved=True)
        self.message_user(request, f'{queryset.count()} comments approved.')
    approve_comments.short_description = "Approve selected comments"
    
    def disapprove_comments(self, request, queryset):
        queryset.update(approved=False)
        self.message_user(request, f'{queryset.count()} comments disapproved.')
    disapprove_comments.short_description = "Disapprove selected comments"