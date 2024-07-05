from __future__ import annotations
from typing import TYPE_CHECKING, List
import logging

from ..models.AnaplanVersion import AnaplanVersion
from ..util.RequestHandler import RequestHandler
from .models.DimensionDetails import DimensionDetails

if TYPE_CHECKING:
    from ..models.AnaplanConnection import AnaplanConnection

logger = logging.getLogger()


class LineItems:
    """
    Class to fetch all line items from a given Anaplan model.
    """

    _handler: RequestHandler = RequestHandler(f"{AnaplanVersion().base_url}/models/")
    _authorization: str
    _endpoint: str
    _dimension: DimensionDetails

    def __init__(self, conn: AnaplanConnection, line_item_id: str):
        """
        ":param conn: Anaplan connection details
        :type conn: : AnaplanConnection
        """
        self._authorization = conn.authorization._auth_token._token_value
        self._endpoint = f"{conn.model}/lineItems/{line_item_id}/dimensions"
        self._dimension = self._get_dimensions()

    @property
    def dimension(self):
        return self._dimension

    def _get_dimensions(self) -> DimensionDetails:
        """
        Fetch all line items from the Anaplan model.

        :return: List of line items
        :rtype: list
        """
        header = {
            "Authorization": f"AnaplanAuthToken {self._authorization}",
            "Accept": f"application/json"
        }

        try:
            dimensions = self._handler.make_request(self._endpoint, "GET", headers=header).json()
        except Exception as e:
            logger.error(f"Error fetching line items: {e}", exc_info=True)
            raise Exception(f"Error fetching line items: {e}")

        if "dimensions" not in dimensions:
            raise KeyError("'dimensions' not found in response")

        return DimensionDetails(dimensions["dimensions"])
