from rest_framework import serializers


def validate_follow_not_self(user, following):
    if user == following:
        raise serializers.ValidationError(
            'Ошибка подписи на самого себя.'
        )


def validate_follow_unique(model, user, following):
    if model.objects.filter(user=user, following=following).exists():
        raise serializers.ValidationError(
            'Ошибка подписи на уже подписанного пользователя.'
        )
