from __future__ import annotations

import os
from flask import Flask
from flask import request
from consumers.user_consumer import UserConsumer
from consumers.phone_numbers_consumer import PhoneNumbersConsumer
from utils import util

app = Flask(__name__)


@app.route("/provider_states/users", methods=["POST"])
def users_provider_states():
    """
    Get the provider state for the users API from the request and perform actions based on it
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
        response = add_user("qe_pact_exists", "qe_pact_exists@example.com")

    return response


@app.route("/provider_states/phone_numbers", methods=["POST"])
def phone_numbers_provider_states():
    """Get the provider state for the phone numbers API and perform actions"""
    provider_state = request.json["state"]

    if provider_state == "a request to reserve phone numbers":
        # delete user if exists
        delete_user("qe_pact_reserve")
        user_details = add_user("qe_pact_reserve", "qe_pact_reserve@example.com")
        session_id = user_details["id"]
        response = reserve_phone_numbers(session_id)

    return response


def delete_user(username):
    """
    Function to delete user if it exists, using the username
    """
    admin_delete_user = UserConsumer(util.PROVIDER_INTERNAL_URL)
    params = {
        "secret": util.ADMIN_SECRET,
        "client_type": util.ADMIN_CLIENT_TYPE,
        "sync": "sync",
    }

    return admin_delete_user.admin_delete_user(
        username, util.request_headers(util.ADMIN_CLIENT_TYPE), params
    )


def add_user(username: str, email: str):
    """
    Function to add a user creating a state of the user already existing
    """
    create_user = UserConsumer(util.PROVIDER_URL)
    payload = {"password": "fake_password", "email": email}

    return create_user.create_user(
        username,
        payload,
        util.ANDROID_CLIENT_TYPE,
        util.request_headers(util.ANDROID_CLIENT_TYPE),
    )


def reserve_phone_numbers(session_id: str):
    """
    Function to reserve TN phone numbers
    """
    phone_numbers = PhoneNumbersConsumer(util.PROVIDER_URL)
    payload = {
        "area_code": "404",
        "reservation_length": "10",
    }

    return phone_numbers.reserve_phone_numbers(
        session_id,
        util.ANDROID_CLIENT_TYPE,
        payload,
        util.request_headers(util.ANDROID_CLIENT_TYPE),
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=os.getenv("FLASK_SERVER_PORT", 5001))
