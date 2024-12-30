from datetime import datetime, timezone
from typing import Any

from bson import ObjectId

from assignment.mongo import MongoModel


class Post(MongoModel):
    collection_name = 'post'
    validations = {
        '$jsonSchema': {
            'bsonType': 'object',
            'required': ['title', 'content', 'author_id', 'created_at'],
            'properties': {
                'title': {'bsonType': 'string'},
                'content': {'bsonType': 'string'},
                'author_id': {'bsonType': 'int'},
                'created_at': {'bsonType': 'date'}
            }
        }
    }

    @classmethod
    def create_post(cls, title: str, content: str, author_id: int) -> Any:
        created_at = datetime.now(tz=timezone.utc)
        post = cls._get_collection().insert_one({
            'title': title,
            'content': content,
            'author_id': author_id,
            'created_at': created_at
        })
        return post.inserted_id

    @classmethod
    def find_by_id(cls, post_id: str) -> dict:
        post = cls._get_collection().find_one({'_id': ObjectId(post_id)})
        return post

    @classmethod
    def update_post(cls, post_id: str, title: str, content: str) -> None:
        return cls._get_collection().update_one({'_id': ObjectId(post_id)}, {'$set': {'title': title, 'content': content}})

    @classmethod
    def get_posts(cls, size: int = 10, order_by: str = 'created_at', order:int = -1, filter_kwargs: dict|None = None, skip_count=0) -> list[dict]:
        collection = cls._get_collection()
        filter_kwargs = filter_kwargs or {}
        cursor = collection.find(filter_kwargs).sort(order_by, order).skip(skip_count).limit(size)
        return list(cursor)

    @classmethod
    def count(cls, filter_kwargs: dict|None = None) -> int:
        filter_kwargs = filter_kwargs or {}
        return cls._get_collection().count_documents(filter_kwargs)

    @classmethod
    def delete_post(cls, post_id: str) -> None:
        return cls._get_collection().delete_one({'_id': ObjectId(post_id)})