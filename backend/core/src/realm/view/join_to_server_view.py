from rest_framework import serializers, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request

from src.realm.daos import ServerDAO
from src.realm.services import JoinToServerService


class JoinToServerSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(read_only=True)
    server_id = serializers.IntegerField(read_only=True)


class JoinToServerView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = JoinToServerSerializer

    def post(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        admin_id = request.user.id

        service = JoinToServerService(
            server_dao=ServerDAO(),
        )
        result = service.execute()
        return Response(result, status=status.HTTP_201_CREATED)