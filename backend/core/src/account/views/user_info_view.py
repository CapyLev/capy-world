from typing import Any

from django.contrib.auth.models import User
from django.http import HttpRequest
from rest_framework import views, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class UserInfoView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(
        self,
        request: HttpRequest,
        *args: Any,
        **kwargs: Any
    ) -> Response:
        user: User = request.user
        user_data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'data_joined': user.date_joined,
        }
        return Response(user_data, status=status.HTTP_201_CREATED)
