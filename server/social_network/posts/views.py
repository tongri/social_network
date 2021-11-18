from datetime import datetime

from django.db.models import Count
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, RetrieveModelMixin, ListModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from dateutil import parser
from rest_framework_simplejwt import views as jwt_views

from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.backends import TokenBackend

from posts.models import Post, Like, MyUser
from posts.serializers import UserSerializer, PostSerializer, LikeSerializer, LikeAmountByDaySerializer, \
    UserActivitySerializer


class JWTTokenObtain(jwt_views.TokenObtainPairView):
    def finalize_response(self, request, response, *args, **kwargs):
        x = 5
        res = super().finalize_response(request, response, *args, **kwargs)
        if res.status_text == 'OK':
            token = response.data['access']
            valid_data = TokenBackend(algorithm='HS256').decode(token, verify=False)
            user = MyUser.objects.get(id=valid_data['user_id'])
            user.last_login = datetime.now()
            user.save()
        return res


class CreateAuth(CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = (AllowAny, )


class PostCreateAPIView(CreateAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()


class LikeViewSet(CreateModelMixin, DestroyModelMixin, GenericViewSet):
    serializer_class = LikeSerializer
    queryset = Like.objects.all()
    http_method_names = ('post', 'delete')

    @action(detail=False, http_method_names=('get', ))
    def analytics(self, request):
        queryset = Like.objects.filter(user=request.user)
        query_params = request.query_params
        date_from_str = query_params.get('date_from')
        date_to_str = query_params.get('date_to')

        if date_from := self.__parse_string_to_date(date_from_str):
            queryset = queryset.filter(date_created__gte=date_from)

        if date_to := self.__parse_string_to_date(date_to_str):
            queryset = queryset.filter(date_created__lte=date_to)

        queryset = queryset.values('date_created').annotate(likes_amount=Count('id'))
        serializer = LikeAmountByDaySerializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def __parse_string_to_date(self, date):
        try:
            result_date = parser.parse(date).date()
        except TypeError:
            return None

        return result_date


class UserActivityRetrieveListViewSet(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    queryset = MyUser.objects.all()
    serializer_class = UserActivitySerializer
