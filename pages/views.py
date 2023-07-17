from django.http import Http404
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from pages.models import BlockPage, Bookmarks, FollowersPage, Page, Post, Comments
from pages.serializers import (
    BookmarksSerializer,
    PageBlockSerializer,
    PagesSerializer,
    PostCreateSerializer,
    PostSerializer, PostDetailSerializer, CommentSerializer, CommentsDetailSerializer,
)


class PagesListView(generics.ListAPIView):
    queryset = Page.objects.all()
    serializer_class = PagesSerializer


class PostsListView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostsCreateView(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        page = serializer.validated_data.get("page")
        title = serializer.validated_data.get("title")
        body = serializer.validated_data.get("body")
        category = serializer.validated_data.get("category")
        user = page.user
        if user != request.user:
            return Response({"status": "Invalid user"})
        post = Post.objects.create(title=title, page=page, body=body)
        post.category.set([category])
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PageBlockView(APIView):
    def post(self, request, *args, **kwargs):
        page_id = kwargs.get("pk", None)
        user = request.user
        page = Page.objects.get(pk=page_id)
        try:
            block_page = BlockPage.objects.get(page=page, user=user)
            block_page.delete()
            return Response({"detail": "page unblocked"}, status=status.HTTP_200_OK)
        except BlockPage.DoesNotExist:
            block_page = BlockPage(page=page, user=user)
            block_page.save()
            return Response({"detail": "page blocked"}, status=status.HTTP_201_CREATED)


class PageBlockedListView(APIView):
    def get(self, request, *args, **kwargs):
        user = request.user
        pages = Page.objects.filter(user=user)
        serializer = PagesSerializer(pages, many=True)
        serialized_data = serializer.data
        return Response(data=serialized_data)


class PageFollowerCreateView(APIView):
    def post(self, request, *args, **kwargs):
        page_id = kwargs.get("pk", None)
        user = request.user
        try:
            followed_page = FollowersPage.objects.get(page_id=page_id, user=user)
            followed_page.delete()
            return Response({"detail": "page unfollow"}, status=status.HTTP_200_OK)
        except FollowersPage.DoesNotExist:
            followed_page = FollowersPage(page_id=page_id, user=user)
            followed_page.save()
            return Response({"detail": "page followed"}, status=status.HTTP_200_OK)


class BookmarksCreateView(APIView):
    def post(self, request, *args, **kwargs):
        post_id = kwargs.get("post_id", None)
        user = request.user
        try:
            bookmarks = Bookmarks.objects.get(user=user, post_id=post_id)
            bookmarks.delete()
            return Response({"detail": "post bookmarks removed"})
        except Bookmarks.DoesNotExist:
            bookmarks = Bookmarks(user=user, post_id=post_id)
            bookmarks.save()
            return Response({"detail": "post bookmarks added"})


class BookmarksListView(generics.ListAPIView):
    queryset = Bookmarks.objects.all()
    serializer_class = BookmarksSerializer

    def get_queryset(self):
        user = self.request.user
        return Bookmarks.objects.filter(user=user)


class PostDetailView(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'slug'

    def get_object(self):
        slug = self.kwargs['slug']
        try:
            post = Post.objects.get(slug__iexact=slug)
            post.views += 1
            post.save()
            return post
        except Post.DoesNotExist:
            raise Http404


class CommentsView(generics.ListAPIView):
    queryset = Comments.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        post_slug = self.kwargs['slug']
        return Comments.objects.filter(post_slug=post_slug)


class CommentListCreateView(generics.ListCreateAPIView):
    queryset = Comments.objects.order_by("-id")
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CommentsDetailSerializer
        return CommentSerializer


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comments.objects.all()
    lookup_field = "id"

    def get_serializer_class(self):
        if self.request.method in ["PUT", "PATCH"]:
            return CommentsDetailSerializer
        return CommentSerializer


class PostLikedView(APIView):
    def post(self, request, slug):
        try:
            post = Post.objects.get(slug=slug)
            user = request.user
            if not user.is_authenticated:
                return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)

            if user in post.liked.all():
                post.liked.remove(user)
                liked = False
            else:
                post.liked.add(user)
                liked = True

            post.save()

            return Response({'liked': liked}, status=status.HTTP_200_OK)
        except Post.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)


class CommentLikedView(APIView):
    def post(self, request, id):
        try:
            comment = Comments.objects.get(id=id)
            user = request.user
            if not user.is_authenticated:
                return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)

            if user in comment.liked.all():
                comment.liked.remove(user)
                liked = False
            else:
                comment.liked.add(user)
                liked = True

            comment.save()

            return Response({'liked': liked}, status=status.HTTP_200_OK)
        except Post.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
