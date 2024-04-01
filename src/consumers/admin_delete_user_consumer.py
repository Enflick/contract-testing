from __future__ import annotations

import requests
from typing import Dict, Any
from src.utils import util


class AdminDeleteUserConsumer:
    """
    Admin delete user consumer class
    """

    def __init__(self, internal_base_uri: str) -> None:
        """
        initialize delete user consumer

        Args:
            internal_base_uri: internal hostname of provider
        """
        self.base_uri = internal_base_uri

    def admin_delete_user(self, username: str, headers: dict) -> Dict[str, Any]:
        """
        Delete a TN user as admin

        Args:
            username: TN username
            headers: headers used in request
        """
        url = f"{self.base_uri}/api2.0/users/{username}"
        params = {
            "secret": util.ADMIN_SECRET,
            "client_type": util.ADMIN_CLIENT_TYPE,
            "sync": "sync",
        }

        response = requests.delete(
            url=url,
            params=params,
            headers=headers,
            timeout=10,
        )
        data: Dict[str, Any] = response.json()

        return data
