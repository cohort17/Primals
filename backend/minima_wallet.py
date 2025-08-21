import requests
import json
import re

MINIMA_API = "http://127.0.0.1:9003"
TOKEN_ID = "0xFA65DA403978B1E4B8A23FEA63BE27793660C1362000FF4042814C12911B1CCC"

def is_valid_address(address):
    return isinstance(address, str) and address.startswith("Mx") and len(address) >= 30

def is_valid_tokenid(tokenid):
    r = re.compile(r"^0x[a-fA-F0-9]{64}$")
    return bool(r.match(tokenid))

def is_valid_amount(amount):
    try:
        val = float(amount)
        return val > 0
    except Exception:
        return False

def call_minima(method, params=None):
    try:
        data = {"method": method}
        if params: data.update(params)
        resp = requests.post(MINIMA_API, json=data, timeout=5)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        print(f"Error calling Minima: {e}")
        return {"error": str(e)}

def create_wallet():
    return call_minima("newaddress")

def import_wallet(mnemonic):
    if not isinstance(mnemonic, str) or len(mnemonic.split()) < 12:
        return {"error": "Invalid mnemonic"}
    return call_minima("importmnemonics", {"mnemonics": mnemonic})

def get_balance(tokenid):
    if not is_valid_tokenid(tokenid):
        return {"error": "Invalid token ID"}
    resp = call_minima("balance")
    for bal in resp.get("response", []):
        if bal.get("tokenid") == tokenid:
            return bal
    return {"balance": 0}

def send_token(address, amount, tokenid):
    if not is_valid_address(address):
        return {"error": "Invalid address"}
    if not is_valid_tokenid(tokenid):
        return {"error": "Invalid token ID"}
    if not is_valid_amount(amount):
        return {"error": "Invalid amount"}
    params = {
        "address": address,
        "amount": amount,
        "tokenid": tokenid
    }
    return call_minima("send", params)

def get_tx_history(address):
    if not is_valid_address(address):
        return {"error": "Invalid address"}
    return call_minima("transactions", {"address": address})

if __name__ == "__main__":
    print("Balance:", get_balance(TOKEN_ID))
