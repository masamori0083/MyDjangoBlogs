from django.contrib import admin
from .models import Post, Comment, Reply, Tag

# Register your models here.


class ReplyInline(admin.StackedInline):
    model = Reply
    extra = 5


class CommentAdmin(admin.ModelAdmin):
    inlines = [ReplyInline]


class PostAdmin(admin.ModelAdmin):
    search_fields = ('title', 'text')
    list_display = ['title', 'is_public',
                    'updated_at', 'created_at', 'title_len']
    list_filter = ['is_public', 'tags']
    ordering = ('-updated_at',)

    def title_len(self, obj):
        return len(obj.title)

    title_len.short_description = 'タイトルの文字数'


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Reply)
admin.site.register(Tag)
