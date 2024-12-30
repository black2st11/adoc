from datetime import datetime, timedelta, timezone

import jwt
from common.exception_code import AuthenticationErrorCode
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from user.dtos.token import InGenerateTokenDto, OutGenerateTokenDto
from user.models.token import RefreshToken

from assignment.exception import CustomException


class TokenService:
    def generate_token(self, dto: InGenerateTokenDto) -> OutGenerateTokenDto:
        if not dto.user and not dto.refresh_token:
            raise CustomException(
                message=_("로그인 정보가 존재하지 않습니다."),
                status_code=401,
                code=AuthenticationErrorCode,
            )
        if dto.user:
            access_token = self._generate_access_token(dto.user.id)
            refresh_token = self._generate_refresh_token(dto.user.id)
            return OutGenerateTokenDto(
                access_token=access_token, refresh_token=refresh_token
            )
        if dto.refresh_token and self._verify_refresh_token(dto.refresh_token):
            return self.refresh_token(dto.access_token, dto.refresh_token)
        raise CustomException(
            message=_("로그인 정보가 존재하지 않습니다."),
            status_code=401,
            code=AuthenticationErrorCode,
        )

    def refresh_token(
        self, access_token: str, refresh_token: str
    ) -> OutGenerateTokenDto:
        user_info = jwt.decode(
            access_token.encode("utf-8"),
            settings.SECRET_KEY,
            options={"verify_exp": False},
            algorithms=["HS256"],
        )
        refresh_token_instance = RefreshToken.objects.filter(
            user_id=user_info["id"], token=refresh_token
        ).first()
        if (
            not refresh_token_instance
            or refresh_token_instance.expired_at < datetime.now(tz=timezone.utc)
        ):
            raise CustomException(
                message=_("로그인 정보가 만료되었습니다."),
                status_code=401,
                code=AuthenticationErrorCode,
            )
        return OutGenerateTokenDto(
            access_token=self._generate_access_token(user_info["id"]),
            refresh_token=self._generate_refresh_token(user_info["id"]),
        )

    def remove_refresh_token(self, access_token: str) -> None:
        user_id = self.verify_access_token(access_token)
        RefreshToken.objects.filter(user_id=user_id).delete()

    @staticmethod
    def verify_access_token(access_token: str) -> int:
        try:
            user_info = jwt.decode(
                access_token.encode("utf-8"), settings.SECRET_KEY, algorithms=["HS256"]
            )
        except jwt.InvalidTokenError:
            raise CustomException(
                message=_("로그인 정보가 만료되었습니다."),
                status_code=401,
                code=AuthenticationErrorCode,
            )
        return user_info["id"]

    @staticmethod
    def _verify_refresh_token(refresh_token: str) -> bool:
        try:
            jwt.decode(
                refresh_token.encode("utf-8"), settings.SECRET_KEY, algorithms=["HS256"]
            )
        except jwt.InvalidTokenError:
            return False
        return True

    @staticmethod
    def _generate_refresh_token(user_id: int) -> str:
        empty_info = {}
        exp = datetime.now(tz=timezone.utc) + timedelta(
            seconds=settings.REFRESH_TOKEN_EXPIRE_SECONDS
        )
        refresh_token = jwt.encode(
            {**empty_info, "exp": exp}, settings.SECRET_KEY, algorithm="HS256"
        )
        RefreshToken.objects.update_or_create(
            user_id=user_id, defaults={"token": refresh_token, "expired_at": exp}
        )
        return refresh_token

    @staticmethod
    def _generate_access_token(user_id: int) -> str:
        user_info = {"id": user_id}
        exp = datetime.now(tz=timezone.utc) + timedelta(
            seconds=settings.ACCESS_TOKEN_EXPIRE_SECONDS
        )
        return jwt.encode(
            {**user_info, "exp": exp}, settings.SECRET_KEY, algorithm="HS256"
        )
