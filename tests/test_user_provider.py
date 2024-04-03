from __future__ import annotations

from multiprocessing import Process
from pact import Verifier
from src.utils import util
from typing import Any, Generator
from yarl import URL

import pytest


def run_server():
    app = util.state_app()
    app.run(debug=True, port=5001)


@pytest.fixture(scope="module")
def user_verifier() -> Generator[Verifier, Any, None]:
    proc = Process(target=run_server, daemon=True)
    verifier = Verifier(
        provider="UserProvider", provider_base_url=str(util.PROVIDER_URL)
    )
    proc.start()
    yield verifier
    proc.kill()


def test_create_user_against_provider(broker: URL, user_verifier: Verifier):
    code, _ = user_verifier.verify_with_broker(
        broker_url=str(broker),
        broker_username=broker.user,
        broker_password=broker.password,
        enable_pending=True,
        publish_version="0.0.1",
        publish_verification_results=True,
        provider_states_setup_url=f"http://localhost:{5001}/provider_states/users",
    )

    assert code == 0
