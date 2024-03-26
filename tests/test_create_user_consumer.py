from __future__ import annotations

import pytest
from pact import Consumer, Provider, Like
from src.consumers.create_user_consumer import CreateUserConsumer
from src.utils import util
from typing import Any, Dict, Generator, TYPE_CHECKING
from yarl import URL

if TYPE_CHECKING:
    from pathlib import Path
    from pact.pact import Pact

MOCK_URL = util.MOCK_URL


@pytest.fixture
def create_user_consumer():
    """ Returns an instance of the CreateUserConsumer class """
    return CreateUserConsumer(str(MOCK_URL))

@pytest.fixture(scope="module")
def create_user_pact(broker: URL, pact_dir: Path) -> Generator[Pact, Any, None]:
    consumer = Consumer("CreateUserConsumer", version=f"2.7.{util.get_git_short_commit_hash()}")
    pact = consumer.has_pact_with(
        Provider("CreateUserProvider"),
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


def test_create_user(create_user_pact: Pact, create_user_consumer: CreateUserConsumer) -> None:
    username = "qe_pact_test2"
    payload = {
        "password": "fake_password",
        "email": f"{username}@example.com",
    }
    headers = util.request_headers(util.IOS_CLIENT_TYPE)
    expected: Dict[str, Any] = {
        "id": "16f5e8815e7550290c912a44ffc73bb7e17cbedf65cc930x280080100018fd51",
        "username": username,
        "guid_hex": "002-02-001-00018fd51",
    }

    (
        create_user_pact.given("a request to create a user with a username that does not exist")
        .upon_receiving(f"a request to create a user with {username} as the username")
        .with_request(
            method="PUT",
            path=f"/api2.0/users/{username}",
            headers=headers,
            query={"client_type": util.IOS_CLIENT_TYPE},
            body=payload,
        )
        .will_respond_with(200, body=Like(expected))
    )

    with create_user_pact:

        create_user_result = create_user_consumer.create_user(username, payload, util.IOS_CLIENT_TYPE, headers)

        assert "id" in create_user_result.keys()
        assert "username" in create_user_result.keys()
        assert "guid_hex" in create_user_result.keys()

        create_user_pact.verify()


def test_user_that_already_exists(create_user_pact: Pact, create_user_consumer: CreateUserConsumer) -> None:
    username = "qe_pact_exists"
    payload = {
        "password": "fake_password",
        "email": f"{username}@example.com",
    }
    headers = util.request_headers(util.ANDROID_CLIENT_TYPE)
    expected: Dict[str, Any] = {
        "result": None,
        "error_code": util.NAME_NOT_AVAILABLE,
        "message": "name already in use",
    }

    (
        create_user_pact.given("a request to create a user that already exists")
        .upon_receiving(f"a request to create a user with {username} as the username")
        .with_request(
            method="PUT",
            path=f"/api2.0/users/{username}",
            headers=headers,
            query={"client_type": util.ANDROID_CLIENT_TYPE},
            body=payload,
        )
        .will_respond_with(400, body=Like(expected))
    )

    with create_user_pact:
        create_user_result = create_user_consumer.create_user(username, payload, util.ANDROID_CLIENT_TYPE, headers)

        assert not create_user_result["result"]
        assert create_user_result["error_code"] == util.NAME_NOT_AVAILABLE
        assert create_user_result["message"] == "name already in use"


