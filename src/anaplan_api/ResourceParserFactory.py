from __future__ import annotations
from typing import Union, TYPE_CHECKING
from .ResourceParserList import ResourceParserList
from .ResourceParserFile import ResourceParserFile
from .transactional.parsers.LineItemParser import LineItemParser
from .transactional.parsers.DimensionsParser import DimensionsParser
from .util.Util import ResourceNotFoundError

if TYPE_CHECKING:
    from .bases.ResourceParserFactory import ResourceParserFactory
    from .transactional.bases.TransactionalParser import TransactionalParser


class ResourceParserGenerator:
    """Factory class for creating ResourceParser objects"""

    def __init__(self, resource: str):
        """
        :param resource: Type of resource to query the specified model for
        :type resource: str
        """
        valid_resources = (
            "imports",
            "exports",
            "actions",
            "processes",
            "files",
            "lists",
            "line_items",
            "dimensions",
        )

        if resource not in valid_resources:
            raise ResourceNotFoundError(
                f"Invalid selection, resource must be one of {', '.join(valid_resources)}"
            )

        self._resource = resource

    def get_parser(self) -> Union[ResourceParserFactory, TransactionalParser]:
        parsers = {
            "files": ResourceParserFile,
            "line_items": LineItemParser,
            "dimensions": DimensionsParser
        }
        return parsers[self._resource] if self._resource in parsers else ResourceParserList
