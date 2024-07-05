from __future__ import annotations
from typing import TYPE_CHECKING, List
import logging

from ..models.AnaplanVersion import AnaplanVersion
from ..util.RequestHandler import RequestHandler

if TYPE_CHECKING:
    from ..models.AnaplanConnection import AnaplanConnection

logger = logging.getLogger()


class LineItems:
    """
    Class to fetch all line items from a given Anaplan model.
    """

    _handler: RequestHandler = RequestHandler(f"{AnaplanVersion().base_url}/models/")
    _authorization: str
    _metadata: bool
    _endpoint: str
    _line_items: List[dict]

    def __init__(self, conn: AnaplanConnection, module_id: str = "", metadata: bool = False):
        """
        ":param conn: Anaplan connection details
        :type conn: : AnaplanConnection
        """
        self._authorization = conn.authorization._auth_token._token_value
        self._endpoint = f"{conn.model}/lineItems" if not module_id else f"{conn.model}/modules/{module_id}/lineItems"
        if metadata:
            self._endpoint = f"{self._endpoint}?includeAll=true"
        self._line_items = self._get_line_items()

    @property
    def line_items(self):
        return self._line_items

    def _get_line_items(self) -> List[dict]:
        """
        Fetch all line items from the Anaplan model.

        :return: Full details of all line items in the specified Anaplan model
        :rtype: LineItemsDetails
        """
        header = {
            "Authorization": f"AnaplanAuthToken {self._authorization}",
            "Accept": f"application/json"
        }

        try:
            line_items = self._handler.make_request(self._endpoint, "GET", headers=header).json()
        except Exception as e:
            logger.error(f"Error fetching line items: {e}", exc_info=True)
            raise Exception(f"Error fetching line items: {e}")

        if "items" not in line_items:
            raise KeyError("'items' not found in response")

        return line_items["items"]
