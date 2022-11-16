import unittest
from memory_document_storage import MemoryDocumentStorage
from service import Service


def create_test_service() -> Service:
    return Service(MemoryDocumentStorage())


class TestService(unittest.TestCase):
    def test_create_document(self):
        service = create_test_service()
        ids = set()
        count_documents = 5
        for i in range(count_documents):
            ids.add(service.CreateDocument(f"test document {i}"))
        documents = service.FindDocuments(ids)
        self.assertEqual(len(documents), count_documents, "Created documents")

    def test_update_document(self):
        service = create_test_service()
        old_title = "title"
        id = service.CreateDocument(old_title)
        ids = set()
        ids.add(id)
        self.assertEqual(service.FindDocuments(ids=ids)[0].get_title(), old_title, "document create with initial title")
        new_title = "42"
        service.EditTitle(id, new_title)
        self.assertEqual(service.FindDocuments(ids=ids)[0].get_title(), new_title, "document update title")
        self.assertEqual(service.FindDocuments(ids=ids)[0].get_body(), "", "document create with initial body")
        new_body = "42 42 42"
        service.EditBody(id, new_body)
        self.assertEqual(service.FindDocuments(ids=ids)[0].get_body(), new_body, "document update body")

    def test_delete_and_restore_document(self):
        service = create_test_service()
        id = service.CreateDocument("test")
        ids = set()
        ids.add(id)
        self.assertEqual(service.FindDocuments(ids=ids, include_deleted=True)[0].__is_deleted__(), False,
                         "create document is deleted")
        service.DeleteDocument(id)
        self.assertEqual(service.FindDocuments(ids=ids, include_deleted=True)[0].__is_deleted__(), True,
                         "document is not deleted")
        service.RestoreDocument(id)
        self.assertEqual(service.FindDocuments(ids=ids, include_deleted=True)[0].__is_deleted__(), False,
                         "document is not restored")

    def test_document_exceptions(self):
        service = create_test_service()
        id = service.CreateDocument("test")
        ids = set()
        ids.add(id)
        with self.assertRaises(Exception) as context:
            service.RestoreDocument(id)
        self.assertEqual(str(context.exception), 'document already restored')

        with self.assertRaises(Exception) as context:
            service.FindDocuments(ids)[0].set_body('x' * 101)
        self.assertEqual(str(context.exception), 'body too large')

        with self.assertRaises(Exception) as context:
            service.FindDocuments(ids)[0].set_title('x' * 51)
        self.assertEqual(str(context.exception), 'title too large')

        service.DeleteDocument(id)
        with self.assertRaises(Exception) as context:
            service.DeleteDocument(id)
        self.assertEqual(str(context.exception), 'document already deleted')

        with self.assertRaises(Exception) as context:
            service.FindDocuments(ids, include_deleted=True)[0].set_body('x' * 10)
        self.assertEqual(str(context.exception), 'document is deleted')


if __name__ == '__main__':
    unittest.main()
