import re
import bcrypt
from django.utils.translation import gettext_lazy as _

from assignment.exception import CustomException
from common.exception_code import ValidationErrorCode
from user.dtos.token import InGenerateTokenDto
from user.dtos.user import InSignupDTO, InLoginDTO
from user.models.user import User
from user.services.token_service import TokenService


class UserService:
    def signup(self, dto:InSignupDTO):
        self._check_email(dto.email)
        if dto.password != dto.re_password:
            raise CustomException(message=_('비밀번호와 확인 비밀번호가 다릅니다.'), status_code=400, code=ValidationErrorCode)
        hashed_password = self._hash_password(dto.password)
        User.objects.create(email=dto.email, hashed_password=hashed_password)

    def login(self, dto: InLoginDTO):
        user = User.objects.filter(email=dto.email).first()
        if not user:
            raise CustomException(message=_('해당 정보를 가지고 있는 유저가 존재하지 않습니다.'), status_code=400, code=ValidationErrorCode)
        if self._match_password(dto.password, user.hashed_password):
            return TokenService().generate_token(InGenerateTokenDto(user=user))
        raise CustomException(message=_('해당 정보를 가지고 있는 유저가 존재하지 않습니다.'), status_code=400, code=ValidationErrorCode)

    @staticmethod
    def logout(access_token: str):
        TokenService().remove_refresh_token(access_token)

    @staticmethod
    def _check_email(email: str):
        if not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
            raise CustomException(message=_('이메일 형식이 올바르지않습니다.'), status_code=400, code=ValidationErrorCode)
        if User.objects.filter(email=email).exists():
            raise CustomException(message=_('이미 존재하는 유저입니다.'), status_code=400, code=ValidationErrorCode)

    @staticmethod
    def _hash_password(password: str) -> str:
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    @staticmethod
    def _match_password(password: str, hashed_password:str) -> bool:
        return bcrypt.checkpw(password.encode('utf-8'),hashed_password.encode('utf-8'))