# Client Types
IOS_CLIENT_TYPE = "TN_IOS_FREE"
ANDROID_CLIENT_TYPE = "TN_ANDROID"
LATEST_APP_VERSION = "24.7.2"

CONTENT_TYPE = "application/json"
SCAR = "bypass_all"

def request_headers(client_type):
    """
    Function that returns request headers depending on the platform user is on
    :param client_type: client type used to make the request
    :return: header object
    """
    if client_type == ANDROID_CLIENT_TYPE:
        user_agent = f"TextNow {LATEST_APP_VERSION} (Pixel 6; Android OS 13; en_US)"
    elif client_type == IOS_CLIENT_TYPE:
        user_agent = f"TextNow/{LATEST_APP_VERSION} (iPhone14,8; iOS 16.5; Scale/3.00)"

    headers = {
        "Content-Type": CONTENT_TYPE,
        "scar": SCAR,
        "user-agent": user_agent,
    }

    return headers
