import pytest

from assignment.exception import CustomException
from community.services.post_service import PostService


class TestPostService:

    @pytest.mark.django_db
    def test_success_create_post_service(self, test_user):
        title = '테스트 제목'
        content = '테스트 내용'
        post_service = PostService()
        post_id = post_service.create_post(
            title=title,
            content=content,
            author_id=test_user.id
        )
        post = post_service.get_post(post_id)
        assert post['_id'] == post_id
        assert post['content'] == content
        assert post['title'] == title

    @pytest.mark.django_db
    def test_fail_create_post_service_by_empty_title(self, test_user):
        title = ''
        content = '테스트 내용'
        post_service = PostService()
        with pytest.raises(CustomException) as e:
            post_service.create_post(
                title=title,
                content=content,
                author_id=test_user.id
            )
        assert e.value.message == '제목을 입력해주세요.'

    @pytest.mark.django_db
    def test_fail_create_post_service_by_empty_title(self, test_user):
        title = '테스트 제목'
        content = ''
        post_service = PostService()
        with pytest.raises(CustomException) as e:
            post_service.create_post(
                title=title,
                content=content,
                author_id=test_user.id
            )
        assert e.value.message == '내용을 입력해주세요.'

    @pytest.mark.django_db
    def test_success_update_post(self, test_user, test_post):
        title = '수정된 테스트 제목'
        content = '수정된 테스트 내용'
        post_service = PostService()
        post_service.update_post(post_id=test_post['_id'], author_id=test_user.id, title=title, content=content)
        post = post_service.get_post(test_post['_id'])
        assert post['title'] == title
        assert post['content'] == content

    @pytest.mark.django_db
    def test_fail_update_post_by_another_author(self, test_user, test_post):
        title = '수정된 테스트 제목'
        content = '수정된 테스트 내용'
        post_service = PostService()
        with pytest.raises(CustomException) as e:
            post_service.update_post(post_id=test_post['_id'], author_id=2, title=title, content=content)
        assert e.value.message == '해당 작업을 할 권한이 없습니다.'

    @pytest.mark.django_db
    def test_success_get_post(self, test_user, test_post):
        post = PostService().get_post(test_post['_id'])
        assert post['_id'] == test_post['_id']
        assert post['content'] == test_post['content']
        assert post['title'] == test_post['title']

    @pytest.mark.django_db
    def test_fail_get_post_by_unregistered_id(self, test_user, test_post):
        with pytest.raises(CustomException) as e:
            PostService().get_post('6771e87d695a6cddc27e38bf')
        assert e.value.message == '해당하는 포스트가 존재하지 않습니다.'

    @pytest.mark.django_db
    def test_success_delete_post(self, test_user, test_post):
        post_service = PostService()
        post_service.delete_post(test_post['_id'], test_user.id)
        with pytest.raises(CustomException) as e:
            PostService().get_post(test_post['_id'])
        assert e.value.message == '해당하는 포스트가 존재하지 않습니다.'

    @pytest.mark.django_db
    def test_fail_delete_post_by_another_author(self, test_user, test_post):
        post_service = PostService()
        with pytest.raises(CustomException) as e:
            post_service.delete_post(test_post['_id'], 2)
        assert e.value.message == '해당 작업을 할 권한이 없습니다.'

    @pytest.mark.django_db
    def test_get_posts(self, test_user, test_posts):
        dto = PostService().get_posts(page=1, size=10)
        assert len(dto.items) == 10
        for idx, post in enumerate(dto.items, start=0):
            assert post['title'] == f'테스트 제목 {20 - idx}'

        dto = PostService().get_posts(page=2, size=10)
        assert len(dto.items) == 10
        for idx, post in enumerate(dto.items, start=0):
            assert post['title'] == f'테스트 제목 {10 - idx}'

    @pytest.mark.django_db
    def test_get_another_author_post(self, test_user, test_posts, test_another_post):
        dto = PostService().get_posts(page=1, size=10, author_id=test_another_post['author_id'])
        assert len(dto.items) == 1
        assert dto.items[0]['_id'] == test_another_post['_id']
        assert dto.items[0]['title'] == test_another_post['title']
        assert dto.items[0]['content'] == test_another_post['content']