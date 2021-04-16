from django.contrib import admin
from posts.models import Post, Group, Comment, Follow


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("text", "pub_date", "author", "group")
    search_fields = ("text",)
    list_filter = ("pub_date",)
    empty_value_display = "-пусто-"


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "description")
    search_fields = ("title",)
    empty_value_display = "-пусто-"


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("post", "author", "text")
    search_fields = ("text", )


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ("user", "author", )
