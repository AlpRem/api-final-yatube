from django.contrib.auth import get_user_model
from rest_framework import serializers

from posts.models import Comment, Follow, Group, Post
from .validators import (validate_follow_not_self,
                                       validate_follow_unique)

User = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'pub_date', 'author', 'image', 'group')
        read_only_fields = ('author', 'pub_date')
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        fields = ('id', 'author', 'post', 'text', 'created')
        read_only_fields = ('author', 'post')
        model = Comment


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'title', 'description', 'slug')
        model = Group


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    following = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username'
    )

    class Meta:
        model = Follow
        fields = ('user', 'following')

    def validate(self, attrs):
        user = self.context['request'].user
        following = attrs['following']
        validate_follow_not_self(user, following)
        validate_follow_unique(Follow, user, following)
        return attrs
