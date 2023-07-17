from rest_framework import serializers

from common.serializers import CategorySerializer
from pages.models import BlockPage, Bookmarks, Page, Post, Comments


class PagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ("id", "name", "slug", "user", "is_organization", "picture", "wide_picture")


class PostSerializer(serializers.ModelSerializer):
    page = PagesSerializer()
    category = CategorySerializer(many=True)

    class Meta:
        model = Post
        fields = ("id", "title", "slug", "body", "page", "views", "updated_at", "category", "image")


class PostDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ("id", "title", "slug",)


class PostCreateSerializer(serializers.ModelSerializer):
    category = serializers.IntegerField()

    class Meta:
        model = Post
        fields = ("id", "title", "slug", "category", "page", "body")


class PageBlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlockPage
        fields = ("id", "user", "page")


class BookmarksSerializer(serializers.ModelSerializer):
    post = PostSerializer()

    class Meta:
        model = Bookmarks
        fields = ("id", "user", "post")


class ChildCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = ("id", "user", "post", "title")


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = ("id", "title", "user", "post", 'parent')


class CommentsDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = ("id", "title", "user", "post", 'parent')
        read_only_fields = ("id",)
