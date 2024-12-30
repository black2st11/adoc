import pytest

from assignment.exception import CustomException
from user.dtos.user import InSignupDTO, InLoginDTO
from user.models.user import User
from user.services.token_service import TokenService
from user.services.user_service import UserService

class TestUserService:

    @pytest.mark.django_db
    def test_success_signup(self):
        email = 'test@test.com'
        password = 'testtest1234'
        re_password = 'testtest1234'
        UserService().signup(InSignupDTO(email=email, password=password, re_password=re_password))
        assert User.objects.filter(email=email).exists()
        assert User.objects.filter(email=email).first().id == 1

    @pytest.mark.django_db
    def test_fail_signup_same_email(self):
        email = 'test@test.com'
        password = 'testtest1234'
        re_password = 'testtest1234'
        UserService().signup(InSignupDTO(email=email, password=password, re_password=re_password))
        with pytest.raises(CustomException) as e:
            UserService().signup(InSignupDTO(email=email, password=password, re_password=re_password))
        assert e.value.message == '이미 존재하는 유저입니다.'

    @pytest.mark.django_db
    def test_fail_signup_password_mismatch(self):
        email = 'test@test.com'
        password = 'testtest1234'
        re_password = 'testtest12345'
        with pytest.raises(CustomException) as e:
            UserService().signup(InSignupDTO(email=email, password=password, re_password=re_password))
        assert e.value.message == '비밀번호와 확인 비밀번호가 다릅니다.'

    @pytest.mark.django_db
    def test_fail_signup_invalid_email(self):
        email = 'test@test'
        password = 'testtest1234'
        re_password = 'testtest1234'
        with pytest.raises(CustomException) as e:
            UserService().signup(InSignupDTO(email=email, password=password, re_password=re_password))
        assert e.value.message == '이메일 형식이 올바르지않습니다.'

    @pytest.mark.django_db
    def test_success_signin(self, test_user):
        email = 'test@test.com'
        password = 'testtest1234'
        result = UserService().login(InLoginDTO(email=email, password=password))
        assert TokenService().verify_access_token(result.access_token)

    @pytest.mark.django_db
    def test_fail_wrong_email_signin(self, test_user):
        email = 'test1@test.com'
        password = 'testtest1234'
        with pytest.raises(CustomException) as e:
            UserService().login(InLoginDTO(email=email, password=password))
        assert e.value.message == '해당 정보를 가지고 있는 유저가 존재하지 않습니다.'

    @pytest.mark.django_db
    def test_fail_wrong_password_signin(self, test_user):
        email = 'test@test.com'
        password = 'testtest1234!'
        with pytest.raises(CustomException) as e:
            UserService().login(InLoginDTO(email=email, password=password))
        assert e.value.message == '해당 정보를 가지고 있는 유저가 존재하지 않습니다.'

    @pytest.mark.django_db
    def test_success_logout(self, test_user):
        email = 'test@test.com'
        password = 'testtest1234'
        result = UserService().login(InLoginDTO(email=email, password=password))
        assert TokenService().verify_access_token(result.access_token)
        UserService().logout(result.access_token)
        with pytest.raises(CustomException) as e:
            TokenService().refresh_token(result.access_token, result.refresh_token)
        assert e.value.message == '로그인 정보가 만료되었습니다.'

