from __future__ import annotations

from flask import Flask
from flask import request
from src.consumers.admin_delete_user_consumer import AdminDeleteUserConsumer
from src.consumers.create_user_consumer import CreateUserConsumer
from src.utils import util

app = Flask(__name__)


@app.route("/provider_states/create_user", methods=["POST"])
def provider_states():
    """
    Get the provider state from the request and perform actions based on it
    """
    provider_state = request.json["state"]

    if (
        provider_state
        == "a request to create a user with a username that does not exist"
    ):
        # delete user if it exists
        username = "qe_pact_test2"
        response = delete_user(username)
    elif provider_state == "a request to create a user that already exists":
        # add user to create a state of a user already existing
        response = add_user()

    return response


def delete_user(username):
    """
    Function to delete user if it exists, using the username
    """
    admin_delete = AdminDeleteUserConsumer(util.PROVIDER_INTERNAL_URL)

    return admin_delete.admin_delete_user(
        username, util.request_headers(util.ADMIN_CLIENT_TYPE)
    )


def add_user():
    """
    Function to add a user creating a state of the user already existing
    """
    create_user = CreateUserConsumer(util.PROVIDER_URL)
    payload = {"password": "fake_password", "email": "qe_pact_exists@example.com"}

    return create_user.create_user(
        "qe_pact_exists",
        payload,
        util.ANDROID_CLIENT_TYPE,
        util.request_headers(util.ANDROID_CLIENT_TYPE),
    )
