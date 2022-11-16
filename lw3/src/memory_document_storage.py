import array

from document_storage_interface import DocumentStorageInterface, Specification


class MemoryDocumentStorage(DocumentStorageInterface):
    def __init__(self):
        self.current_id = 0
        self.storage = {}

    def next_id(self) -> int:
        id = self.current_id
        self.current_id = self.current_id + 1
        return id

    def get_document(self, spec: Specification) -> array:
        result = []
        for document in self.storage.values():
            if document.id in spec.ids:
                if not spec.include_deleted and document.deleted_at is None:
                    result.append(document)
                elif spec.include_deleted:
                    result.append(document)
        if spec.ids is not None:
            tmp = []
            for document in result:
                if document.id in spec.ids:
                    tmp.append(document)
            result = tmp
        return result

    def store_document(self, documents: array):
        for document in documents:
            self.storage[document.id] = document
