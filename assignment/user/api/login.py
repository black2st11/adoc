from rest_framework.response import Response
from rest_framework.views import APIView

from user.dtos.user import InLoginDTO
from user.services.user_service import UserService


class LoginAPIView(APIView):
    def post(self, request):
        email=request.data.get('email')
        password=request.data.get('password')
        dto = UserService().login(InLoginDTO(email=email, password=password))
        return Response(status=200, data={'access_token': dto.access_token, 'refresh_token': dto.refresh_token})