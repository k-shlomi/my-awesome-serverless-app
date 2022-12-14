import os
from typing import Dict, Optional

import requests

USER_ID = "user-2"
USER_NAME = "my-user"


def get_deployment_url() -> str:
    raw = [l.strip().split(" - ")[-1] for l in os.popen("sls info --stage local").readlines() if "http" in l]
    raw = [l for l in raw if " " not in l]
    if not raw:
        raise Exception("No deployment url found")
    return raw[0]


BASE_URL = f"{get_deployment_url()}/users"


def create_user() -> Optional[Dict]:
    payload = {
        "user_id": USER_ID,
        "user_name": USER_NAME,
    }
    response = requests.post(BASE_URL, json=payload)
    if response.status_code != 404:
        return response.json()
    return None


def get_user() -> Optional[Dict]:
    response = requests.get(BASE_URL + f"/{USER_ID}")
    if response.status_code != 404:
        return response.json()
    return None


if __name__ == '__main__':
    user = get_user()
    if not user:
        print("User doesn't exist")
        user = create_user()
        print(f"User created: {user}")
    else:
        print(f"Got user from DB: {user}")
