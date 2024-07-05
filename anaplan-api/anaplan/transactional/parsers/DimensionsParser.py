from typing import List
from ..bases.TransactionalParser import TransactionalParser
from ..models.DimensionDetails import DimensionDetails


class DimensionsParser(TransactionalParser):
    _raw_response: List[dict]
    _details: List[DimensionDetails]

    def __init__(self, response: List[dict]):
        self._raw_response = response
        self._details = [DimensionDetails(**item) for item in response]

    @property
    def details(self) -> List[DimensionDetails]:
        return self._details
