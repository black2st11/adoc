import time

import pytest
from django.conf import settings

from assignment.mongo import MongoDB
from community.services.post_service import PostService
from user.dtos.user import InSignupDTO
from user.models import User
from user.services.user_service import UserService


@pytest.fixture
@pytest.mark.django_db
def test_user():
    UserService().signup(InSignupDTO(email='test@test.com', password='testtest1234', re_password='testtest1234'))
    return User.objects.get(email='test@test.com')

@pytest.fixture
@pytest.mark.django_db
def test_another_user():
    UserService().signup(InSignupDTO(email='another@test.com', password='testtest1234', re_password='testtest1234'))
    return User.objects.get(email='another@test.com')

@pytest.fixture(autouse=True)
def mongodb_cleanup():
    yield
    db = MongoDB().connect()
    db.client.drop_database(settings.MONGODB_DATABASE_NAME)

@pytest.fixture
def test_post(test_user):
    title = '테스트 제목'
    content = '테스트 내용'
    post_service = PostService()
    post_id = post_service.create_post(
        title=title,
        content=content,
        author_id=test_user.id
    )
    return post_service.get_post(post_id)


@pytest.fixture
def test_posts(test_user):
    post_service = PostService()
    for i in range(1, 21):
        title = f'테스트 제목 {i}'
        content = f'테스트 내용 {i}'
        post_service.create_post(
            title=title,
            content=content,
            author_id=test_user.id
        )
        time.sleep(0.01)

@pytest.fixture
def test_another_post(test_another_user):
    post_service = PostService()
    title = f'테스트 다른 제목'
    content = f'테스트 다른 내용'
    post_id = post_service.create_post(
        title=title,
        content=content,
        author_id=test_another_user.id
    )
    return post_service.get_post(post_id)