from django.contrib import admin

from common.models import Quiz, Choice, Category


@admin.register(Quiz)
class UserAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active']


@admin.register(Category)
class UserAdmin(admin.ModelAdmin):
    list_display = ['title']


