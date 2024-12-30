from typing import Any
from django.utils.translation import gettext_lazy as _

from assignment.exception import CustomException
from common.dto import PaginationItem
from common.exception_code import ValidationErrorCode, AuthorizationErrorCode, NotFoundErrorCode
from community.models.post import Post


class PostService:
    def __init__(self):
        self.collection = Post()

    def create_post(self, title: str, content: str, author_id: int) -> str:
        self._validate_data(title, content)
        return str(self.collection.create_post(title, content, author_id))

    def get_post(self, post_id: Any):
        if post:= self.collection.find_by_id(post_id):
            return {**post, '_id': str(post['_id'])}
        raise CustomException(message=_('해당하는 포스트가 존재하지 않습니다.'), status_code=404, code=NotFoundErrorCode)

    def get_posts(self, page: int = 1, size: int = 10, order_by: str = 'created_at', order: int = -1, author_id: int | None = None) -> PaginationItem:
        filter_kwargs = {'author_id': author_id} if author_id else {}
        total = self.collection.count(filter_kwargs)
        skip_count = (page - 1) * size
        documents = self.collection.get_posts(size=size, order_by=order_by, order= order, filter_kwargs=filter_kwargs, skip_count=skip_count)

        return PaginationItem(
            total=total,
            items=[{**document, '_id': str(document['_id'])} for document in  documents],
            size=size,
            page=page,
            total_page=(total + size - 1) // size
        )

    def update_post(self, post_id: Any, author_id:int, title: str, content: str):
        self._validate_data(title, content)
        post = self.collection.find_by_id(post_id)
        if post.get('author_id') != author_id:
            raise CustomException(message=_('해당 작업을 할 권한이 없습니다.'), status_code=403, code=AuthorizationErrorCode)
        return self.collection.update_post(post_id=post_id, title=title, content=content)

    def delete_post(self, post_id: Any, author_id: int):
        post = self.collection.find_by_id(post_id)
        if post.get('author_id') != author_id:
            raise CustomException(message=_('해당 작업을 할 권한이 없습니다.'), status_code=403, code=AuthorizationErrorCode)
        return self.collection.delete_post(post_id)

    @staticmethod
    def _validate_data(title: str, content: str):
        if not title:
            raise CustomException(message=_('제목을 입력해주세요.'), status_code=400 ,code=ValidationErrorCode)
        if not content:
            raise CustomException(message=_('내용을 입력해주세요.'), status_code=400, code=ValidationErrorCode)