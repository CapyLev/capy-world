from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from ..daos import ServerDAO
from ..services import GetUserServersService


class GetUserServersView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request: Request, *args, **kwargs) -> Response:
        user: User = request.user

        service = GetUserServersService(server_dao=ServerDAO())
        result = service.execute(
            user_id=user.id,
        )
        return Response(result, status=status.HTTP_200_OK)
