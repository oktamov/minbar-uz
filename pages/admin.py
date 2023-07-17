from django.contrib import admin

from pages.models import BlockPage, Bookmarks, FollowersPage, Page, Post, Comments, Complaints


@admin.register(Page)
class UserAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "user"]


@admin.register(Post)
class UserAdmin(admin.ModelAdmin):
    list_display = ["title", "slug", "page"]


@admin.register(BlockPage)
class UserAdmin(admin.ModelAdmin):
    list_display = ["user", "page"]


@admin.register(FollowersPage)
class UserAdmin(admin.ModelAdmin):
    list_display = ["user", "page"]


@admin.register(Bookmarks)
class UserAdmin(admin.ModelAdmin):
    list_display = ["user", "post"]


@admin.register(Comments)
class UserAdmin(admin.ModelAdmin):
    list_display = ["user", "title"]


@admin.register(Complaints)
class UserAdmin(admin.ModelAdmin):
    list_display = ["text", "page", "post"]

