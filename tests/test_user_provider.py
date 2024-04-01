from __future__ import annotations

from multiprocessing import Process
from pact import Verifier
from src.utils import util
from typing import Any, Generator
from yarl import URL

import pytest

PROVIDER_URL = util.PROVIDER_URL


@pytest.fixture(scope="module")
def create_user_verifier() -> Generator[Verifier, Any, None]:
    # start the state app as a separate process
    proc = Process(target=util.start_state_app, daemon=True)
    verifier = Verifier(provider="UserProvider", provider_base_url=str(PROVIDER_URL))
    proc.start()
    yield verifier
    proc.kill()


def test_create_user_against_provider(broker: URL, create_user_verifier: Verifier):
    code, _ = create_user_verifier.verify_with_broker(
        broker_url=str(broker),
        broker_username=broker.user,
        broker_password=broker.password,
        enable_pending=True,
        publish_version="0.0.1",
        publish_verification_results=True,
        provider_states_setup_url="http://localhost:5001/provider_states/create_user",
    )

    assert code == 0
