import requests
import re

MINIMA_API = "http://127.0.0.1:9003"
TOKEN_ID = "0xFA65DA403978B1E4B8A23FEA63BE27793660C1362000FF4042814C12911B1CCC"


def is_valid_address(address):
     return ( isinstance(address, str) and
             address.startswith("Mx") and
             len(address) >= 30 )

def is_valid_tokenid(tokenid):
    r = re.compile(r"^0x[a-fA-F0-9]{64}$")
    return bool(r.match(tokenid))

def call_minima(method, params=None):
    try:
        data = {"method": method}
        if params:
            data.update(params)
        resp = requests.post(MINIMA_API, json=data, timeout=5)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        print(f"Error calling Minima: {e}")
        return {"error": str(e)}

def mint_nft(owner_address, metadata, tokenid):
    if not is_valid_address(owner_address):
        return {"error": "Invalid address"}
    if not is_valid_tokenid(tokenid):
        return {"error": "Invalid token ID"}
    if not isinstance(metadata, str) or len(metadata) < 4:
        return {"error": "Invalid metadata"}
    params = {
        "address": owner_address,
        "amount": 1,
        "tokenid": tokenid,
        "data": metadata
    }
    return call_minima("send", params)

if __name__ == "__main__":
    owner = "Mx..."  # Replace with a valid Minima address
    metadata = "ipfs://Qm..."
    print(mint_nft(owner, metadata, TOKEN_ID))
