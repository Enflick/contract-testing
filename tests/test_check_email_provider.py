from __future__ import annotations

from pact import Verifier
from typing import Any, Generator
from yarl import URL

import pytest

PROVIDER_URL = URL("https://api.stage.textnow.me")


@pytest.fixture(scope="module")
def verifier() -> Generator[Verifier, Any, None]:
    verifier = Verifier(
        provider="CheckEmailProvider",
        provider_base_url=str(PROVIDER_URL)
    )

    yield verifier


def test_check_email_exists_against_broker(broker: URL, verifier: Verifier):
    code, _ = verifier.verify_with_broker(
        broker_url=str(broker),
        broker_username=broker.user,
        broker_password=broker.password,
        enable_pending=True,
        publish_verification_results=True,
    )

    assert code == 0