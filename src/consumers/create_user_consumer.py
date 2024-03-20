from __future__ import annotations

import requests
from typing import Dict, Any

class CreateUserConsumer:
    """
    Create user consumer class
    """

    def __init__(self, base_uri: str) -> None:
        """
        initialize consumer

        Args:
        base_uri: hostname of provider
        """
        self.base_uri = base_uri

    def create_user(self, username: str, password: str, client_type: str, headers: dict) -> Dict[str, Any]:
        """
        Create a TN user

        Args:
            username: TN username
            password: user password
            client_type: client type
            headers: headers used in request
        """
        url = f"{self.base_uri}/api2.0/users/{username}"
        params = {"client_type": client_type}
        response = requests.put(
            url=url,
            json={"password": password},
            params=params,
            headers=headers,
            timeout=10,
        )
        data: Dict[str, Any] = response.json()

        return data
