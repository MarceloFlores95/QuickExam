from abc import ABCMeta, abstractmethod
from pylatex import Document


class PDF(metaclass=ABCMeta):

    @abstractmethod
    def append_to_document(doc : Document) -> None:
        pass
