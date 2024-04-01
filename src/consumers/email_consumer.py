from __future__ import annotations

import requests

from src.textnow_result import TextNowResult
from typing import Dict, Any


class EmailConsumer:
    """
    Check email consumer class to check if an email exists
    """

    def __init__(self, base_uri: str) -> None:
        """
        initialize consumer

        Args:
        base_uri: hostname of provider
        """
        self.base_uri = base_uri

    def get_email(self, email: str, client_type: str, headers: dict) -> TextNowResult:
        """
        Check if an email exists

        Args: client_type: client type used in making request
        """
        url = f"{self.base_uri}/api2.0/emails/{email}"
        response = requests.get(
            url=url, params={"client_type": client_type}, headers=headers, timeout=10
        )
        data: Dict[str, Any] = response.json()

        return TextNowResult(
            result=data["result"],
            error_code=data["error_code"],
            message=None,
        )
