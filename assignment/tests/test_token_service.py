from datetime import datetime, timedelta, timezone

import pytest
from freezegun import freeze_time
from user.dtos.token import InGenerateTokenDto
from user.services.token_service import TokenService

from assignment.exception import CustomException


class TestTokenService:

    @pytest.mark.django_db
    def test_success_generate_token_by_user(self, test_user):
        token_service = TokenService()
        result = token_service.generate_token(InGenerateTokenDto(user=test_user))
        assert result.access_token
        assert result.refresh_token
        assert token_service.verify_access_token(result.access_token)

    @pytest.mark.django_db
    def test_success_generate_token_by_refresh_token(self, test_user):
        token_service = TokenService()
        ret = token_service.generate_token(InGenerateTokenDto(user=test_user))
        result = token_service.generate_token(
            InGenerateTokenDto(
                access_token=ret.access_token, refresh_token=ret.refresh_token
            )
        )

        assert result.access_token
        assert result.refresh_token
        assert token_service.verify_access_token(result.access_token)

    @pytest.mark.django_db
    def test_fail_generate_token(self, test_user):
        with pytest.raises(CustomException) as e:
            TokenService().generate_token(InGenerateTokenDto())
        assert e.value.message == "로그인 정보가 존재하지 않습니다."

    @pytest.mark.django_db
    def test_success_verify_access_token(self, test_user):
        token_service = TokenService()
        result = token_service.generate_token(InGenerateTokenDto(user=test_user))
        assert token_service.verify_access_token(result.access_token)

    @pytest.mark.django_db
    def test_fail_verify_access_token_by_exp(self, test_user):
        initial_datetime = datetime.now(tz=timezone.utc)
        test_datetime = initial_datetime + timedelta(hours=1, minutes=1)
        with freeze_time(initial_datetime) as frozen_datetime:
            token_service = TokenService()
            result = token_service.generate_token(InGenerateTokenDto(user=test_user))
            frozen_datetime.move_to(test_datetime)
            with pytest.raises(CustomException) as e:
                assert token_service.verify_access_token(result.access_token)
            assert e.value.message == "로그인 정보가 만료되었습니다."

    @pytest.mark.django_db
    def test_success_refresh_token(self, test_user):
        token_service = TokenService()
        ret = token_service.generate_token(InGenerateTokenDto(user=test_user))
        result = token_service.refresh_token(ret.access_token, ret.refresh_token)
        assert result.access_token
        assert result.refresh_token

    @pytest.mark.django_db
    def test_success_refresh_token_by_exp_access_token(self, test_user):
        initial_datetime = datetime.now(tz=timezone.utc)
        test_datetime = initial_datetime + timedelta(hours=1, minutes=1)
        with freeze_time(initial_datetime) as frozen_datetime:
            token_service = TokenService()
            ret = token_service.generate_token(InGenerateTokenDto(user=test_user))
            frozen_datetime.move_to(test_datetime)
            result = token_service.refresh_token(ret.access_token, ret.refresh_token)
            assert token_service.verify_access_token(result.access_token)

    @pytest.mark.django_db
    def test_success_refresh_token_by_exp_refresh_token(self, test_user):
        initial_datetime = datetime.now(tz=timezone.utc)
        test_datetime = initial_datetime + timedelta(days=15)
        with freeze_time(initial_datetime) as frozen_datetime:
            token_service = TokenService()
            ret = token_service.generate_token(InGenerateTokenDto(user=test_user))
            frozen_datetime.move_to(test_datetime)
            with pytest.raises(CustomException) as e:
                token_service.refresh_token(ret.access_token, ret.refresh_token)
            assert e.value.message == "로그인 정보가 만료되었습니다."
