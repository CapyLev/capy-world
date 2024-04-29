from rest_framework import serializers, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from ..daos import ServerDAO
from ..models import Server
from ..services import CreateServerService


class CreateServerSerializer(serializers.ModelSerializer):
    description = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    class Meta:
        model = Server
        fields = (
            "id",
            "name",
            "description",
        )


class CreateServerView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CreateServerSerializer

    def post(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        admin_id = request.user.id

        service = CreateServerService(server_dao=ServerDAO())
        result = service.execute(
            admin_id=admin_id,
            name=serializer.validated_data.get("name"),
            description=serializer.validated_data.get("description"),
        )
        return Response(result, status=status.HTTP_201_CREATED)
