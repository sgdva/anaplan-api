from abc import ABC, abstractmethod
from typing import List


class TransactionalParser(ABC):
    """
    Base class for all Transactional API parsers
    """
    _raw_response: List[dict]
    _details: list

    @abstractmethod
    def __init__(self, response: List[dict]):
        pass

    @abstractmethod
    def details(self):
        pass
