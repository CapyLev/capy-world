from typing import Any

from django.contrib.auth.models import User
from django.http import HttpRequest
from rest_framework import serializers, views, status
from rest_framework.response import Response


class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "password",
            "email",
        )
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data: dict[str, Any]) -> User:
        return User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
        )


class RegisterUserView(views.APIView):
    serializers_class = RegisterUserSerializer

    def post(
        self,
        request: HttpRequest,
        *args: Any,
        **kwargs: Any
    ) -> Response:
        serializer = self.serializers_class(data=request.data)

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
