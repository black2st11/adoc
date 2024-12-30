from rest_framework.response import Response
from rest_framework.views import APIView

from user.services.token_service import TokenService


class RefreshAPIView(APIView):
    def post(self, request):
        access_token = request.headers.get('Authorization').split(' ')[1]
        refresh_token = request.data.get('refresh_token')
        dto = TokenService().refresh_token(access_token, refresh_token)
        return Response(status=200, data={'access_token': dto.access_token, 'refresh_token': dto.refresh_token})