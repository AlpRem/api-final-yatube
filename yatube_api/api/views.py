from rest_framework import viewsets

from posts.models import Comment, Group, Post

from .pagination import PostPagination
from .permissions import PostAndCommentPermission
from .serializers import CommentSerializer, GroupSerializer, PostSerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.select_related('author').all()
    serializer_class = PostSerializer
    permission_classes = (PostAndCommentPermission,)
    pagination_class = PostPagination

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