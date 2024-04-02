from __future__ import annotations

import requests
from typing import Dict, Any


class PhoneNumbersConsumer:
    """
    Creates a phone numbers consumer class
    """

    def __init__(self, base_uri: str) -> None:
        """
        initialize the phone numbers consumer

        Args:
        base_uri: hostname of provider
        """
        self.base_uri = base_uri

    def reserve_phone_numbers(
        self, session_id: str, client_id: str, payload: dict, headers: dict
    ) -> Dict[str, Any]:
        """
        Reserve a list of numbers. This is when a list of available phone numbers are displayed to the user

        Args:
            session_id: user session id used when making the request
            client_id: client type
            payload: contains the area_code and reservation_length values
            headers: headers used in request
        """
        url = f"{self.base_uri}/api2.0/phone_numbers/reserve"
        params = {
            "client_id": session_id,
            "client_type": client_id,
        }
        response = requests.post(
            url=url,
            json=payload,
            params=params,
            headers=headers,
            timeout=10,
        )
        data: Dict[str, Any] = response.json()

        return data
