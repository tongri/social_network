from django.contrib.auth.models import User
from rest_framework import serializers

from posts.models import Post, Like, MyUser


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = MyUser
        fields = ('id', 'username', 'password')

    def create(self, validated_data):
        return MyUser.objects.create_user(**validated_data)


class PostSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Post
        fields = ('id', 'author', 'title', 'text')


class LikeSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Like
        fields = ('user', 'post')


class LikeAmountByDaySerializer(serializers.Serializer):
    date_created = serializers.DateField()
    likes_amount = serializers.IntegerField()


class UserActivitySerializer(serializers.ModelSerializer):

    class Meta:
        model = MyUser
        fields = ('id', 'username', 'last_login', 'last_action')
