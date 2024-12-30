from rest_framework.response import Response
from rest_framework.views import APIView

from user.services.user_service import UserService


class LogoutAPIView(APIView):
    def post(self, request):
        access_token = request.headers.get('Authorization').split(' ')[1]
        UserService().logout(access_token)
        return Response(status=200, data={"message": '로그아웃이 성공하였습니다.'})