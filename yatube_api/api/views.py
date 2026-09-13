from rest_framework import viewsets

from posts.models import Comment, Group, Post

from .permissions import PostAndCommentPermission
from .serializers import CommetSerializer, GroupSerializer, PostSerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.select_related('author').all()
    serializer_class = PostSerializer
    permission_classes = (PostAndCommentPermission,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)