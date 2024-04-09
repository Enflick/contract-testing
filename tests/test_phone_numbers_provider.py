from __future__ import annotations

from pact import Verifier
from src.utils import util
from typing import Any, Generator
from yarl import URL

import pytest


@pytest.fixture(scope="module")
def phone_numbers_verifier() -> Generator[Verifier, Any, None]:
    verifier = Verifier(
        provider="PhoneNumbersProvider", provider_base_url=str(util.PROVIDER_URL)
    )
    yield verifier


def test_phone_numbers_against_provider(broker: URL, phone_numbers_verifier: Verifier):
    code, _ = phone_numbers_verifier.verify_with_broker(
        broker_url=str(broker),
        broker_username=broker.user,
        broker_password=broker.password,
        enable_pending=True,
        publish_version="0.0.1",
        publish_verification_results=True,
        provider_states_setup_url="http://localhost:5001/provider_states/phone_numbers",
    )

    assert code == 0
