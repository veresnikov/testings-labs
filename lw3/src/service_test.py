import unittest
from document import Document
from mock_document_storage import MockDocumentStorage, Specification
from service import Service


def init() -> (Service, MockDocumentStorage):
    mock_storage = MockDocumentStorage()
    return Service(mock_storage), mock_storage


class TestService(unittest.TestCase):
    def test_create_document(self):
        service, mock_storage = init()
        service.CreateDocument("test document")
        result = mock_storage.get_document(Specification())
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].get_title(), "test document")
        self.assertEqual(result[0].get_body(), "")

    def test_delete_document(self):
        service, mock_storage = init()
        id = mock_storage.next_id()
        mock_storage.set_documents([Document(id, "test document", "")])
        service.DeleteDocument(id)
        result = mock_storage.get_document(Specification())
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].__is_deleted__(), True)

    def test_restore_document(self):
        service, mock_storage = init()
        id = mock_storage.next_id()
        doc = Document(id, "test document", "")
        doc.delete()
        mock_storage.set_documents([doc])
        service.RestoreDocument(id)
        result = mock_storage.get_document(Specification())
        self.assertEqual(result[0].__is_deleted__(), False)

    def test_set_title(self):
        service, mock_storage = init()
        id = mock_storage.next_id()
        mock_storage.set_documents([Document(id, "test document", "")])
        service.EditTitle(id, "new title")
        result = mock_storage.get_document(Specification())
        self.assertEqual(result[0].get_title(), "new title")

    def test_set_body(self):
        service, mock_storage = init()
        id = mock_storage.next_id()
        mock_storage.set_documents([Document(id, "test document", "test body")])
        service.EditBody(id, "new body")
        result = mock_storage.get_document(Specification())
        self.assertEqual(result[0].get_body(), "new body")


if __name__ == '__main__':
    unittest.main()
