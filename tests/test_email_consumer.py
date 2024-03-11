from __future__ import annotations

import pytest
import logging
from src.utils import util

from http import HTTPStatus
from src.textnow_result import TextNowResult

import requests
from pact import Consumer, Provider, Format, Like
from src.check_email_consumer import CheckEmailConsumer
from typing import Any, Dict, Generator, TYPE_CHECKING
from yarl import URL

if TYPE_CHECKING:
    from pathlib import Path
    from pact.pact import Pact

log = logging.getLogger(__name__)
MOCK_URL = URL("http://localhost:8080")

@pytest.fixture()
def email_consumer():
    """ Returns an instance of the CheckEmailConsumer class """
    return CheckEmailConsumer(str(MOCK_URL))

@pytest.fixture(scope="module")
def pact(broker: URL, pact_dir: Path) -> Generator[Pact, Any, None]:
    """ Set up Pact """
    consumer = Consumer("CheckEmailConsumer")
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
    expected: Dict[str: Any] = {
        "result": None,
        "error_code": None,
    }

    (
        pact.given("an email kabuki@example.com does not exist")
        .upon_receiving("a request to get email kabuki@example.com")
        .with_request("get", "/api2.0/emails/kabuki@example.com")
        .will_respond_with(404, body=Like(expected))
    )

    with pact:

        get_email_result = email_consumer.get_email("kabuki@example.com", util.ANDROID_CLIENT_TYPE, headers)

        assert isinstance(get_email_result, TextNowResult)
        assert not get_email_result.result
        assert not get_email_result.error_code

        pact.verify()


def test_check_email_that_exists(pact: Pact, email_consumer: CheckEmailConsumer) -> None:
    headers = util.request_headers(util.IOS_CLIENT_TYPE)
    expected: Dict[str, Any] = {
        "result": None,
        "error_code": None,
    }

    (
        pact.given("an email grandvasier@example.com that already exists")
        .upon_receiving("a request to get the email grandvasier@example.com")
        .with_request("get", "/api2.0/emails/grandvasier@example.com")
        .will_respond_with(200, body=Like(expected))
    )

    with pact:
        get_email_result = email_consumer.get_email("grandvasier@example.com", util.IOS_CLIENT_TYPE, headers)

        assert isinstance(get_email_result, TextNowResult)
        assert not get_email_result.result
        assert not get_email_result.error_code

        pact.verify()


