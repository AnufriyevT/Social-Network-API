from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings

from .models import UserProfile, Post, Like


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = (
            "id",
            "first_name",
            "last_name",
            "email",
            "last_login",
            "last_request",
        )


class PostSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = (
            "text",
            "pub_date",
            "author",
            "likes",
        )

    @swagger_serializer_method(
        serializer_or_field=serializers.CharField(help_text="Amount of likes")
    )
    def get_likes(self, obj: Post):
        return obj.like_set.count()


class LikePostSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(write_only=True, required=True)

    class Meta:
        model = Post
        fields = ("user_id",)

    def update(self, instance: Post, validated_data):
        user_id = validated_data["user_id"]
        user = UserProfile.objects.get(id=user_id)
        Like.objects.get_or_create(post=instance, user=user)
        return instance


class UnlikePostSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(write_only=True, required=True)

    class Meta:
        model = Post
        fields = ("user_id",)

    def update(self, instance: Post, validated_data):
        user_id = validated_data["user_id"]
        user = UserProfile.objects.get(id=user_id)
        Like.objects.filter(post=instance, user=user).delete()
        return instance


class UserSerializerWithToken(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()
    password = serializers.CharField(write_only=True)

    def get_token(self, obj):
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(obj)
        token = jwt_encode_handler(payload)

        return token

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)

        instance.save()

        return instance

    class Meta:
        model = UserProfile
        fields = ("token", "username", "first_name", "last_name", "password")


class LikeSerializer(serializers.Serializer):
    date = serializers.DateField(source="pub_date__date")
    likes_count = serializers.IntegerField()

    def create(self, validated_data):
        raise NotImplementedError

    def update(self, instance, validated_data):
        raise NotImplementedError
