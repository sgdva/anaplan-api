from typing import List
from ..bases.TransactionalParser import TransactionalParser
from ..models.LineItemDetails import LineItemsDetails


class LineItemParser(TransactionalParser):
    _raw_response: List[dict]
    _details: List[LineItemsDetails]

    def __init__(self, response: List[dict]):
        self._raw_response = response
        self._details = [LineItemsDetails(**item) for item in response]

    @property
    def details(self) -> List[LineItemsDetails]:
        return self._details
