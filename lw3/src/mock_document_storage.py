import array
from memory_document_storage import MemoryDocumentStorage, Specification


class MockDocumentStorage(MemoryDocumentStorage):
    def __init__(self):
        super().__init__()
        self.mock_documents = []

    def set_documents(self, documents: array):
        self.mock_documents = documents

    def get_document(self, spec: Specification) -> array:
        return self.mock_documents

    def store_document(self, documents: array):
        self.mock_documents = documents
