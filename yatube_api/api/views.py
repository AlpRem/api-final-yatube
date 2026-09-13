from rest_framework import filters, mixins, permissions, viewsets

from posts.models import Comment, Follow, Group, Post

from .pagination import PostPagination
from .permissions import PostAndCommentPermission
from .serializers import (
    CommentSerializer,
    FollowSerializer,
    GroupSerializer,
    PostSerializer,
)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.select_related('author').all()
    serializer_class = PostSerializer
    permission_classes = (PostAndCommentPermission,)
    pagination_class = PostPagination

    def paginate_queryset(self, queryset):
        if (
                'limit' not in self.request.query_params
                and 'offset' not in self.request.query_params
        ):
            return None
        return super().paginate_queryset(queryset)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (PostAndCommentPermission,)
    lookup_url_kwarg = 'comment_id'

    def get_queryset(self):
        return Comment.objects.select_related(
            'author',
            'post'
        ).filter(post_id=self.kwargs['post_id'])

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            post_id=self.kwargs['post_id']
        )


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (permissions.AllowAny,)


class FollowViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = FollowSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def get_queryset(self):
        return Follow.objects.filter(
            user=self.request.user
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
