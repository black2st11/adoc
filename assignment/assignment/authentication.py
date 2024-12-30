from common.exception_code import AuthenticationErrorCode
from django.utils.translation import gettext_lazy as _
from rest_framework.authentication import BaseAuthentication
from user.services.token_service import TokenService

from assignment.exception import CustomException


class JWTAuthentication(BaseAuthentication):
    VALID_TOKEN_TYPE = "bearer"

    def authenticate(self, request):
        if auth := request.headers.get("Authorization"):
            try:
                access_token = auth.split(" ")[1]
                user_id = TokenService().verify_access_token(access_token)
                request.user_id = user_id
                return user_id, access_token
            except IndexError:
                raise CustomException(
                    message=_("로그인 정보가 만료되었습니다."),
                    status_code=401,
                    code=AuthenticationErrorCode,
                )
        request.user_id = None
        return None, None
