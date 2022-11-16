import array

from document import Document
from document_storage_interface import DocumentStorageInterface, Specification


class Service:
    def __init__(self, storage: DocumentStorageInterface):
        self.storage = storage

    def CreateDocument(self, title) -> int:
        id = self.storage.next_id()
        self.storage.store_document([Document(id, title, "")])
        return id

    def EditTitle(self, id: int, new_title: str):
        ids = set()
        ids.add(id)
        document = self.storage.get_document(Specification(ids=ids))[0]
        document.set_title(new_title)
        self.storage.store_document([document])

    def EditBody(self, id: int, new_body: str):
        ids = set()
        ids.add(id)
        document = self.storage.get_document(Specification(ids=ids))[0]
        document.set_body(new_body)
        self.storage.store_document([document])

    def DeleteDocument(self, id: int):
        ids = set()
        ids.add(id)
        document = self.storage.get_document(Specification(ids=ids, include_deleted=True))[0]
        document.delete()
        self.storage.store_document([document])

    def RestoreDocument(self, id: int):
        ids = set()
        ids.add(id)
        document = self.storage.get_document(Specification(ids=ids, include_deleted=True))[0]
        document.restore()
        self.storage.store_document([document])

    def FindDocuments(self, ids: set = None, include_deleted: bool = None) -> array:
        return self.storage.get_document(Specification(ids, include_deleted))
