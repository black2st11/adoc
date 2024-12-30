from pymongo import MongoClient
from pymongo.errors import CollectionInvalid

from django.conf import settings


class MongoDB:
    client = None
    db = None

    @classmethod
    def connect(cls):
        if cls.client is None:
            cls.client = MongoClient(settings.MONGODB_URL)
            cls.db = cls.client[settings.MONGODB_DATABASE_NAME]
        return cls.db

    @classmethod
    def close(cls):
        if cls.client is not None:
            cls.client.close()
            cls.client = None
            cls.db = None

class MongoModel:
    collection_name = None
    validator = None

    @classmethod
    def _get_collection(cls):
        db = MongoDB.connect()

        if cls.collection_name not in db.list_collection_names():
            try:
                kwargs = {'validator': cls.validator} if cls.validator else {}
                db.create_collection(cls.collection_name, **kwargs)
            except CollectionInvalid:
                pass
        return db[cls.collection_name]
