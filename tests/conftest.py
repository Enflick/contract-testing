from __future__ import annotations

from pathlib import Path
from typing import Any, Generator, Union

import pytest
from testcontainers.compose import DockerCompose
from yarl import URL

PACT_DIR = Path(__file__).parent.resolve()


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--broker-url",
        help="URL of broker to use. If option given, the container will not be started",
        type=str,
    )


@pytest.fixture(scope="session")
def broker(request: pytest.FixtureRequest) -> Generator[URL, Any, None]:
    """
    Fixture to run the Pact broker
    """
    broker_url: Union[str, None] = request.config.getoption("--broker-url")

    if broker_url:
        yield URL(broker_url)
        return
    with DockerCompose() as _:
        yield URL("http://pactbroker:pactbroker@localhost:9292")
        return


@pytest.fixture(scope="session")
def pact_dir() -> Path:
    return PACT_DIR / "pacts"
