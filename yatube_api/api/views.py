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