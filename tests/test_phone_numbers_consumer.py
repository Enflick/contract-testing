from __future__ import annotations

import pytest
from pact import Consumer, Provider, Like, EachLike
from src.consumers.phone_numbers_consumer import PhoneNumbersConsumer
from src.utils import util
from typing import Any, Dict, Generator, TYPE_CHECKING
from yarl import URL

if TYPE_CHECKING:
    from pathlib import Path
    from pact.pact import Pact

MOCK_URL = util.get_mock_url()


@pytest.fixture()
def phone_numbers_consumer():
    """Returns an instance of the PhoneNumberConsumer class"""
    return PhoneNumbersConsumer(str(MOCK_URL))


@pytest.fixture(scope="session")
def phone_numbers_pact(broker: URL, pact_dir: Path) -> Generator[Pact, Any, None]:
    consumer = Consumer(
        "PhoneNumbersConsumer", version=f"1.0.5.{util.get_git_short_commit_hash()}"
    )
    pact = consumer.has_pact_with(
        Provider("PhoneNumbersProvider"),
        pact_dir=pact_dir,
        publish_to_broker=True,
        host_name=MOCK_URL.host,
        port=MOCK_URL.port,
        broker_base_url=str(broker),
        broker_username=broker.user,
        broker_password=broker.password,
    )

    pact.start_service()
    yield pact
    pact.stop_service()


def test_reserve_phone_numbers(
    phone_numbers_pact: Pact, phone_numbers_consumer: PhoneNumbersConsumer
) -> None:
    username = "qe_pact_reserve"
    session_id = "16f5e8815e7550290c912a44ffc73bb7e17cbedf65cc930x280080100018fd51"
    payload = {"area_code": "404", "reservation_length": "10"}
    headers = util.request_headers(util.ANDROID_CLIENT_TYPE)
    params = {
        "client_type": util.ANDROID_CLIENT_TYPE,
        "client_id": session_id,
    }

    expected: Dict[str, Any] = {
        "result": {
            "reservation_id": "88495d40030fc7c5",
            "phone_numbers": EachLike(
                "7052439308",
                minimum=2,  # we expect there to be a minimum of 2 reserved numbers
            ),
        },
        "error_code": None,
    }
    (
        phone_numbers_pact.given("a request to reserve phone numbers")
        .upon_receiving(f"a request to reserve phone numbers from a user - {username}")
        .with_request(
            method="POST",
            path="/api2.0/phone_numbers/reserve",
            headers=headers,
            query=params,
            body=payload,
        )
        .will_respond_with(200, body=Like(expected))
    )

    with phone_numbers_pact:
        reserve_phone_numbers = phone_numbers_consumer.reserve_phone_numbers(
            session_id, util.ANDROID_CLIENT_TYPE, payload, headers
        )

        assert isinstance(reserve_phone_numbers["result"]["reservation_id"], str)
        assert isinstance(reserve_phone_numbers["result"]["phone_numbers"], list)
        assert not reserve_phone_numbers["error_code"]

        phone_numbers_pact.verify()


def test_assign_phone_number(
    phone_numbers_pact: Pact, phone_numbers_consumer: PhoneNumbersConsumer
) -> None:
    username = "qe_pact_assign"
    session_id = "16f5e8815e7550290c912a44ffc73bb7e17cbedf65cc930x280080100018fd29"
    payload = {"reservation_id": "88495d40030fc7c5", "phone_number": "7059996138"}
    params = {
        "client_id": session_id,
        "client_type": util.IOS_CLIENT_TYPE,
    }
    headers = util.request_headers(util.IOS_CLIENT_TYPE)

    expected: Dict[str, Any] = {
        "result": {"phone_number": "7059996138"},
        "error_code": None,
    }

    (
        phone_numbers_pact.given("a request to assign a given phone number")
        .upon_receiving(f"a request to assign a phone number to a user - {username}")
        .with_request(
            method="POST",
            path="/api2.0/phone_numbers/assign_reserved",
            headers=headers,
            query=params,
            body=payload,
        )
        .will_respond_with(200, body=Like(expected))
    )

    with phone_numbers_pact:
        assign_phone_numbers = phone_numbers_consumer.assign_phone_number(
            params, payload, headers
        )

        assert isinstance(assign_phone_numbers["result"]["phone_number"], str)
        assert not assign_phone_numbers["error_code"]

        phone_numbers_pact.verify()
