from rest_framework.response import Response
from rest_framework.views import APIView
from user.dtos.user import InSignupDTO
from user.services.user_service import UserService


class SignupAPIView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        re_password = request.data.get("re_password")
        UserService().signup(
            InSignupDTO(email=email, password=password, re_password=re_password)
        )
        return Response(status=201, data={"message": "회원가입이 완료되었습니다."})
