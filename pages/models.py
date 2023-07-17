from django.db import models
from django.utils.text import slugify

from common.models import Category
from users.models import User


class Page(models.Model):
    name = models.CharField(max_length=15)
    slug = models.CharField(max_length=20, blank=True)
    is_organization = models.BooleanField(default=False)
    bio = models.TextField(blank=True)
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, related_name="page")
    picture = models.ImageField(upload_to="static/images/", blank=True, null=True)
    wide_picture = models.ImageField(upload_to="static/images/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.name.upper():
            self.slug = slugify(self.name.lower())
        return super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=55)
    slug = models.CharField(max_length=70, blank=True)
    category = models.ManyToManyField(Category, blank=True, related_name="post")
    body = models.TextField(blank=True)
    page = models.ForeignKey(Page, blank=True, null=True, on_delete=models.CASCADE, related_name="post")
    image = models.ImageField(upload_to="static/images/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    views = models.IntegerField(default=0)
    liked = models.ManyToManyField(User, default=None, blank=True, related_name='liked_post')

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.title.upper():
            self.slug = slugify(self.title.lower())
        return super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return self.title


class BlockPage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="block_page")
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name="block_page")


class FollowersPage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers_page")
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name="followers_page")


class Bookmarks(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookmarks")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="bookmarks")


class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    title = models.CharField(max_length=500)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, blank=True, null=True, related_name="child_comments")
    liked = models.ManyToManyField(User, default=None, blank=True, related_name='liked_comments')


class Complaints(models.Model):
    text = models.CharField(max_length=255, blank=True)
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name="complaints")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="complaints")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
