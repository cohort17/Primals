import requests
import json
from typing import Dict, Any, Union

# This is a placeholder base URL for the Minima node's API.
# In a real-world application, this would be configured to point to your running Minima node.
MINIMA_API_URL = "http://localhost:9002"

def get_status() -> Dict[str, Any]:
    """
    Fetches the current status of the Minima node.
    This is useful for checking if the node is running and synchronized.
    """
    try:
        response = requests.get(f"{MINIMA_API_URL}/status")
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching Minima status: {e}")
        return {"error": str(e)}

def get_balance(address: str = None) -> Union[Dict[str, Any], None]:
    """
    Fetches the balance for a specific address or all balances if no address is provided.
    
    Args:
        address (str): The Minima address to check the balance for.
                       If None, it fetches the balances for all addresses.
    """
    try:
        if address:
            params = {"address": address}
            response = requests.get(f"{MINIMA_API_URL}/balance", params=params)
        else:
            response = requests.get(f"{MINIMA_API_URL}/balance")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching balance: {e}")
        return None

def send_transaction(recipient_address: str, amount: float, token_id: str = "0x00") -> Dict[str, Any]:
    """
    Sends a transaction from the wallet to a recipient.
    
    Args:
        recipient_address (str): The Minima address of the recipient.
        amount (float): The amount of tokens to send.
        token_id (str): The ID of the token to send. Default is "0x00" for Minima.
    """
    try:
        # The 'send' command requires URL-encoding. The requests library handles this.
        params = {
            "address": recipient_address,
            "amount": amount,
            "tokenid": token_id
        }
        
        # The Minima API endpoint for sending a transaction is 'send'.
        response = requests.get(f"{MINIMA_API_URL}/send", params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error sending transaction: {e}")
        return {"error": str(e)}

# --- Example Usage (simulated) ---
if __name__ == '__main__':
    print("--- Minima Wallet Module Test ---")

    # Simulate fetching the node status
    status = get_status()
    if "error" in status:
        print(f"Failed to connect to Minima node. Please ensure it is running at {MINIMA_API_URL}.")
    else:
        print(f"Node Status: {status.get('mini_sync_chain_length', 'N/A')} blocks synchronized.")

    # Simulate fetching balances
    test_address = "Mx1234567890abcdef1234567890abcdef12345678"
    all_balances = get_balance()
    if all_balances:
        print("\nAll Balances:")
        print(json.dumps(all_balances, indent=4))
    
    # Simulate sending a transaction
    # Note: This will fail if a node isn't running, which is expected for this demo.
    send_result = send_transaction(
        recipient_address="Mx_RecipientAddress_123456789",
        amount=5.5,
        token_id="0x00"
    )
    if "error" in send_result:
        print(f"\nSimulated send transaction failed (expected without a running node): {send_result['error']}")
    else:
        print("\nSimulated send transaction result:")
        print(json.dumps(send_result, indent=4))
