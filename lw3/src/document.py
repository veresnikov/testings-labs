import time

MAX_BODY_SIZE = 100
MAX_TITLE_SIZE = 50


class Document:
    def __init__(self, id: int, title: str, body: str):
        self.id = id
        self.title = title
        self.body = body
        self.created_at = time.time()
        self.updated_at = self.created_at
        self.deleted_at = None

    def set_body(self, body: str):
        self.__assert_operation__()
        if len(body) > MAX_BODY_SIZE:
            raise OverflowError('body too large')
        self.body = body
        self.updated_at = time.time()

    def get_body(self) -> str:
        return self.body

    def set_title(self, title: str):
        self.__assert_operation__()
        if len(title) > MAX_TITLE_SIZE:
            raise OverflowError('title too large')
        self.title = title
        self.updated_at = time.time()

    def get_title(self) -> str:
        return self.title

    def delete(self):
        if self.__is_deleted__():
            raise RuntimeError('document already deleted')
        self.deleted_at = time.time()
        self.updated_at = self.deleted_at

    def restore(self):
        if not self.__is_deleted__():
            raise RuntimeError('document already restored')
        self.deleted_at = None
        self.updated_at = self.deleted_at

    def __is_deleted__(self) -> bool:
        return self.deleted_at is not None

    def __assert_operation__(self):
        if self.__is_deleted__():
            raise RuntimeError('document is deleted')
