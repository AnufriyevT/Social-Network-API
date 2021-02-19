from django.db.models import Count
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from .models import Post, UserProfile, Like
from .serializers import (
    PostSerializer,
    LikeSerializer,
    LikePostSerializer,
    UnlikePostSerializer,
    UserSerializer,
    UserSerializerWithToken,
)
from .filters.filters import LikeFilterSet


class NetworkViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(operation_summary="Update post")
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="like",
        method="POST",
        request_body=UserSerializer,
        responses={200: LikePostSerializer()},
    )
    @action(detail=True, methods=["POST"])
    def like(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = LikePostSerializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, "_prefetched_objects_cache", None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="unlike",
        method="POST",
        request_body=UserSerializer,
        responses={200: UnlikePostSerializer},
    )
    @action(detail=True, methods=["POST"])
    def unlike(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = UnlikePostSerializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, "_prefetched_objects_cache", None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


class UserViewSet(
    viewsets.GenericViewSet, ListModelMixin, RetrieveModelMixin, CreateModelMixin
):
    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary="create user",
        request_body=UserSerializer,
        responses={200: UserSerializerWithToken()},
    )
    def create(self, request, *args, **kwargs):
        serializer = UserSerializerWithToken(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    @action(detail=False, methods=["GET"])
    def current_user(self, request):
        """

        Determine the current user by their token, and return their data

        """
        serializer = self.get_serializer(request.user)

        return Response(serializer.data)


class LikeViewSet(viewsets.GenericViewSet, ListModelMixin):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = LikeFilterSet

    @swagger_auto_schema(operation_summary="analytics", responses={200: LikeSerializer})
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        aggregated_qs = queryset.values("pub_date__date").annotate(
            likes_count=Count("pub_date")
        )
        serializer = LikeSerializer(instance=aggregated_qs, many=True)
        return Response(serializer.data)
