from django.urls import path

from pages.views import (
    BookmarksCreateView,
    PageBlockedListView,
    PageBlockView,
    PageFollowerCreateView,
    PagesListView,
    PostsCreateView,
    PostsListView, PostDetailView, CommentListCreateView, CommentDetailView, PostLikedView, CommentLikedView,
    BookmarksListView,
)

urlpatterns = [
    path("list", PagesListView.as_view(), name="page-list"),
    path("post/list", PostsListView.as_view(), name="post-list"),
    path("post/<slug:slug>/", PostDetailView.as_view(), name="post-detail"),
    path("post/create", PostsCreateView.as_view(), name="post-create"),
    path("<int:pk>/block-unblock/create", PageBlockView.as_view(), name="page-block-unblock"),
    path("blocked/list", PageBlockedListView.as_view(), name="page-blocked-list"),
    path("<int:pk>/follow-unfollow/create", PageFollowerCreateView.as_view(), name="page-follow-unfollow"),
    path("post/<int:post_id>/bookmarks/create", BookmarksCreateView.as_view(), name="page-bookmarks"),
    path("post/bookmarks/list", BookmarksListView.as_view(), name="page-bookmarks-list"),
    path("post/<slug:slug>/comment/", CommentListCreateView.as_view(), name="post-comment-list"),
    path("post/comment/<int:id>", CommentDetailView.as_view(), name="post-comment-list"),
    path("post/<slug:slug>/liked", PostLikedView.as_view(), name="post-liked"),
    path("post/comment/<int:id>/liked", CommentLikedView.as_view(), name="post-liked"),
]
