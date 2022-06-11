from django.shortcuts import get_object_or_404

from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users.models import Subscribe, User
from users.serializers import UserSubscribeSerializer

ALREADY_SUBSCRIBED_ERROR = {'errors': 'Вы уже подписаны на автора!'}
NOT_SIGNED_ERROR = {'errors': 'Вы не подписаны на данного автора!'}
SUBSCRIBE_YOURSELF_ERROR = {'errors': 'Нельзя подписаться на самого себя!'}
UNSUBSCRIBE_YOURSELF_ERROR = {'errors': 'Нельзя отписаться от самого себя!'}


class CustomUserViewSet(UserViewSet):
    @action(detail=False,
            permission_classes=(IsAuthenticated,),
            name='subscriptions')
    def subscriptions(self, request):
        queryset = (User.objects.filter(following__user=request.user).
                    prefetch_related('recipes'))
        return Response(
            UserSubscribeSerializer(
                queryset, many=True, context={'request': request}
            ).data,
            status=status.HTTP_200_OK
        )

    @action(methods=['POST', 'DELETE'], detail=True, name='subscribe')
    def subscribe(self, request, id):
        author = get_object_or_404(User, id=id)
        user = request.user
        if user == author:
            return Response(
                SUBSCRIBE_YOURSELF_ERROR if request.method == 'POST'
                else UNSUBSCRIBE_YOURSELF_ERROR
            )
        if request.method == 'POST':
            subscription, created = Subscribe.objects.get_or_create(
                user=user, author=author
            )
            if created:
                return Response(
                    UserSubscribeSerializer(
                        subscription.author, context={'request': request}
                    ).data,
                    status=status.HTTP_201_CREATED)
            return Response(ALREADY_SUBSCRIBED_ERROR,
                            status=status.HTTP_400_BAD_REQUEST)
        subscription = Subscribe.objects.filter(user=user, author=author)
        if subscription.exists():
            subscription.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(NOT_SIGNED_ERROR, status=status.HTTP_400_BAD_REQUEST)
