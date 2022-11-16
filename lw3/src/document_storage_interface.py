import array
from abc import ABCMeta, abstractmethod


class Specification:
    def __init__(self, ids: set = None, include_deleted: bool = None):
        self.ids = ids
        self.include_deleted = include_deleted


class DocumentStorageInterface:
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_document(self, spec: Specification) -> array:
        """find documents by specification"""

    @abstractmethod
    def store_document(self, documents: array):
        """store documents"""

    @abstractmethod
    def next_id(self) -> int:
        """generate next number id"""
