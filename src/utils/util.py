import contextlib
import os
import socket
from subprocess import check_output
from yarl import URL

# Client Types
IOS_CLIENT_TYPE = "TN_IOS_FREE"
ANDROID_CLIENT_TYPE = "TN_ANDROID"
ADMIN_CLIENT_TYPE = "TN_ADMIN"
ADMIN_SECRET = os.getenv("TN_ADMIN_SECRET")
LATEST_APP_VERSION = "24.7.2"
# error codes
NAME_NOT_AVAILABLE = "NAME_NOT_AVAILABLE"
PARAMETER_REQUIRED = "PARAMETER_REQUIRED"

CONTENT_TYPE = "application/json"
SCAR = "bypass_all"

# MOCK_URL = URL("http://localhost:8080")
PROVIDER_URL = URL("https://api.stage.textnow.me")
PROVIDER_INTERNAL_URL = URL("https://api-private.stage.us-east-1.textnow.io")


def request_headers(client_type: str):
    """
    Function that returns request headers depending on the platform user is on
    :param client_type: client type used to make the request
    :return: header object
    """
    if client_type == ANDROID_CLIENT_TYPE:
        user_agent = f"TextNow {LATEST_APP_VERSION} (Pixel 6; Android OS 13; en_US)"
    elif client_type == IOS_CLIENT_TYPE:
        user_agent = f"TextNow/{LATEST_APP_VERSION} (iPhone14,8; iOS 16.5; Scale/3.00)"
    elif client_type == ADMIN_CLIENT_TYPE:
        user_agent = "Go-http-client/2.0"

    headers = {
        "Content-Type": CONTENT_TYPE,
        "scar": SCAR,
        "user-agent": user_agent,
    }

    return headers


def get_git_short_commit_hash() -> str:
    """
    Function to get the short git commit hash which we use for versioning
    """
    return check_output(["git", "rev-parse", "--short", "HEAD"]).decode("ascii").strip()


def find_free_port() -> int:
    """
    Helper function to find a free port. This is so that we don't run into conflicts
    """
    with contextlib.closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(("", 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        return s.getsockname()[1]


def get_mock_url() -> URL:
    """
    Function that returns a mock URL for testing consumer contracts
    """
    return URL(f"http://localhost:{find_free_port()}")
