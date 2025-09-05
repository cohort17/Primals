import requests

MINIMA_API = "http://127.0.0.1:9003"


def lock_tokens_for_bridge(address, amount, tokenid, bridge_address):
    params = {
        "address": bridge_address,
        "amount": amount,
        "tokenid": tokenid,
        "state": "LOCKED_FOR_BRIDGE"
    }
    return requests.post(
        MINIMA_API,
        json={"method": "send", **params}
    ).json()
