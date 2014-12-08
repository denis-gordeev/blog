from django.contrib import admin
from blog.models import BlogPost, Commentary, Vote, UserProfile

class CommentaryInline(admin.StackedInline):
    model = Commentary

class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'excerpt', 'created', 'author')
    list_filter = ['created', 'author']
    date_hierarchy = 'created'
    search_fields = ['title', 'body', 'author__username', 'author__first_name', 'author__last_name']
    inlines = [CommentaryInline]
admin.site.register(BlogPost, BlogPostAdmin)

class VoteAdmin(admin.ModelAdmin):
    pass
admin.site.register(Vote, VoteAdmin)

class CommentaryAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'created')
    list_filter = ['created', 'author']
    search_fields = ['author', 'body', 'post__title']
admin.site.register(Commentary, CommentaryAdmin)

admin.site.register(UserProfile)
