import json
import requests
import os

class MinimaWallet:
    """
    Manages interactions with a Minima wallet via its REST API.
    """

    def __init__(self, api_host='http://127.0.0.1:9001'):
        self.api_host = api_host
        # The API key can be stored as an environment variable or a config file.
        # This will need to be configured for production environments.
        self.api_key = os.getenv('MINIMA_API_KEY')

    def _call_api(self, endpoint, payload=None):
        """
        A private method to handle API calls to the Minima node.
        """
        headers = {
            'Content-Type': 'application/json',
            'X-Api-Key': self.api_key
        }
        url = f"{self.api_host}/{endpoint}"
        
        try:
            response = requests.post(url, data=json.dumps(payload), headers=headers)
            response.raise_for_status()  # This will raise an HTTPError for bad responses (4xx or 5xx)
            return response.json()
        except requests.exceptions.HTTPError as err:
            print(f"HTTP Error: {err}")
            return None
        except requests.exceptions.RequestException as err:
            print(f"Request Error: {err}")
            return None

    def get_balance(self):
        """
        Retrieves the current balance of the Minima wallet.
        """
        # TODO: Implement the logic to call the Minima API's 'balance' endpoint
        # The API documentation for Minima will specify the exact payload and endpoint.
        # You should parse the response to extract the token balances.
        print("Getting balance...")
        # Placeholder for API call
        # response = self._call_api('balance')
        # if response and 'status' in response and response['status'] == 'success':
        #     return response['response']
        return "Balance retrieval not yet implemented."

    def send_token(self, recipient_address, amount, token_id="0x00"):
        """
        Sends a specified amount of a token to a recipient address.
        :param recipient_address: The Minima address of the recipient.
        :param amount: The amount of the token to send.
        :param token_id: The unique identifier of the token.
        """
        # TODO: Implement the logic to call the Minima API's 'send' or similar endpoint.
        # Ensure you handle the response and confirm the transaction was successful.
        print(f"Sending {amount} of token {token_id} to {recipient_address}...")
        # Placeholder for API call
        # payload = {
        #     "to": recipient_address,
        #     "amount": amount,
        #     "tokenid": token_id
        # }
        # response = self._call_api('send', payload)
        # if response and 'status' in response and response['status'] == 'success':
        #     return response['response']
        return "Send functionality not yet implemented."

    def get_transaction_history(self):
        """
        Retrieves the transaction history for the Minima wallet.
        """
        # TODO: Implement the logic to call the Minima API's 'history' endpoint
        # and parse the transaction history data.
        print("Getting transaction history...")
        # Placeholder for API call
        # response = self._call_api('history')
        # if response and 'status' in response and response['status'] == 'success':
        #     return response['response']
        return "Transaction history retrieval not yet implemented."

    def get_wallet_address(self):
        """
        Retrieves the main wallet address.
        """
        # TODO: Implement a method to get the wallet address.
        # This is a critical first step for the UI.
        print("Getting wallet address...")
        return "Wallet address retrieval not yet implemented."

if __name__ == '__main__':
    # This block allows you to run this file directly for testing.
    # To run, you must have a Minima node running with a valid API key.
    # Set the MINIMA_API_KEY environment variable.
    wallet = MinimaWallet()
    
    # Example usage:
    # balance = wallet.get_balance()
    # print(f"Wallet balance: {balance}")
    
    # history = wallet.get_transaction_history()
    # print(f"Wallet history: {history}")
    
