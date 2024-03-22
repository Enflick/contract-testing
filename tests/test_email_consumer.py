from __future__ import annotations

import pytest
import logging
from src.utils import util

from src.textnow_result import TextNowResult

from pact import Consumer, Provider, Like
from src.consumers.check_email_consumer import CheckEmailConsumer
from typing import Any, Dict, Generator, TYPE_CHECKING
from yarl import URL

if TYPE_CHECKING:
    from pathlib import Path
    from pact.pact import Pact

log = logging.getLogger(__name__)
MOCK_URL = util.MOCK_URL

@pytest.fixture()
def email_consumer():
    """ Returns an instance of the CheckEmailConsumer class """
    return CheckEmailConsumer(str(MOCK_URL))

@pytest.fixture(scope="module")
def pact(broker: URL, pact_dir: Path) -> Generator[Pact, Any, None]:
    """ Set up Pact """
    consumer = Consumer("CheckEmailConsumer", version=f"1.2.{util.get_git_short_commit_hash()}")
    pact = consumer.has_pact_with(
        Provider("CheckEmailProvider"),
        pact_dir=pact_dir,
        publish_to_broker=True,
        # Mock service configuration
        host_name=MOCK_URL.host,
        port=MOCK_URL.port,
        # Broker configuration
        broker_base_url=str(broker),
        broker_username=broker.user,
        broker_password=broker.password,
    )

    pact.start_service()
    yield pact
    pact.stop_service()


def test_check_email_does_not_exist(pact: Pact, email_consumer: CheckEmailConsumer) -> None:
    headers = util.request_headers(util.ANDROID_CLIENT_TYPE)
    email_address = "kabuki@example.com"
    expected: Dict[str: Any] = {
        "result": None,
        "error_code": None,
    }

    (
        pact.given(f"an email {email_address} does not exist")
        .upon_receiving(f"a request to get email {email_address}")
        .with_request(
            method="GET",
            path=f"/api2.0/emails/{email_address}",
            headers=headers,
            query={"client_type": util.ANDROID_CLIENT_TYPE},
        )
        .will_respond_with(404, body=Like(expected))
    )

    with pact:

        get_email_result = email_consumer.get_email(email_address, util.ANDROID_CLIENT_TYPE, headers)

        assert isinstance(get_email_result, TextNowResult)
        assert not get_email_result.result
        assert not get_email_result.error_code

        pact.verify()


def test_check_email_that_exists(pact: Pact, email_consumer: CheckEmailConsumer) -> None:
    headers = util.request_headers(util.IOS_CLIENT_TYPE)
    email_address = "static_10@example.com"
    expected: Dict[str, Any] = {
        "result": None,
        "error_code": None,
    }

    (
        pact.given(f"an email {email_address} that already exists")
        .upon_receiving(f"a request to get the email {email_address}")
        .with_request(
            method="GET",
            path=f"/api2.0/emails/{email_address}",
            headers=headers,
            query={"client_type": util.IOS_CLIENT_TYPE},
        )
        .will_respond_with(200, body=Like(expected))
    )

    with pact:
        get_email_result = email_consumer.get_email(email_address, util.IOS_CLIENT_TYPE, headers)

        assert isinstance(get_email_result, TextNowResult)
        assert not get_email_result.result
        assert not get_email_result.error_code

        pact.verify()


