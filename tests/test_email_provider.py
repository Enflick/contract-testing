from __future__ import annotations

from pact import Verifier
from src.utils import util
from typing import Any, Generator
from yarl import URL

import pytest


@pytest.fixture(scope="module")
def check_email_verifier() -> Generator[Verifier, Any, None]:
    verifier = Verifier(
        provider="EmailProvider", provider_base_url=str(util.PROVIDER_URL)
    )

    yield verifier


def test_check_email_exists_against_broker(broker: URL, check_email_verifier: Verifier):
    code, _ = check_email_verifier.verify_with_broker(
        broker_url=str(broker),
        broker_username=broker.user,
        broker_password=broker.password,
        enable_pending=True,
        publish_version="0.0.1",
        publish_verification_results=True,
    )

    assert code == 0
