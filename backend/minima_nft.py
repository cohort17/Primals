import json
import requests
from typing import Dict, Any, List

class MinimaNFTModule:
    """
    A class to handle all NFT-related interactions with a Minima node.

    This module provides functions for minting, transferring, and querying
    NFTs by communicating with a Minima node's API.
    """

    def __init__(self, minima_api_url: str):
        """
        Initializes the NFT module with the Minima node API URL.
        """
        self.api_url = minima_api_url
        print(f"Minima NFT module initialized for API: {self.api_url}")

    def _call_minima_api(self, endpoint: str, payload: Dict[str, Any]) -> Any:
        """
        Private helper function to make a POST request to the Minima node's API.
        """
        url = f"{self.api_url}/{endpoint}"
        try:
            response = requests.post(url, json=payload, timeout=5)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error calling Minima API: {e}")
            return {"status": False, "error": str(e)}

    def mint_nft(self, owner_address: str, nft_name: str, description: str) -> Dict[str, Any]:
        """
        Mints a new NFT on the Minima blockchain.
        
        Args:
            owner_address: The Minima address that will own the new NFT.
            nft_name: The name of the NFT.
            description: A brief description of the NFT.

        Returns:
            A dictionary with the result of the minting process.
        """
        print(f"Attempting to mint NFT: '{nft_name}' for address: {owner_address}")
        
        # A real NFT mint would require more complex metadata and possibly an image.
        # This is a simplified example of the 'createtoken' command.
        payload = {
            "name": nft_name,
            "description": description,
            "minima_address": owner_address,
            "nft": True,
            "total_supply": 1,
            "token_decimals": 0
        }
        
        # In a real scenario, this would call the Minima node's 'createtoken' endpoint.
        # For this example, we simulate a successful response.
        print("Simulating API call to create NFT token...")
        
        # Simulating a transaction hash
        mock_tx_hash = "0x" + "abcdef1234567890" * 4 
        return {
            "status": True,
            "message": f"NFT '{nft_name}' successfully minted.",
            "tokenid": "0x1234567890abcdef" * 4,
            "transaction_hash": mock_tx_hash
        }

    def transfer_nft(self, sender_address: str, receiver_address: str, token_id: str) -> Dict[str, Any]:
        """
        Transfers an NFT from one Minima address to another.
        
        Args:
            sender_address: The current owner of the NFT.
            receiver_address: The recipient address.
            token_id: The unique ID of the NFT to transfer.
        
        Returns:
            A dictionary with the result of the transfer.
        """
        print(f"Attempting to transfer NFT {token_id} from {sender_address} to {receiver_address}")

        # In a real scenario, this would call the Minima node's 'send' endpoint.
        # We simulate the process.
        payload = {
            "to": receiver_address,
            "amount": "1",
            "tokenid": token_id
        }
        print("Simulating API call to transfer token...")
        
        mock_tx_hash = "0x" + "fedcba9876543210" * 4
        return {
            "status": True,
            "message": f"NFT {token_id} transfer initiated.",
            "transaction_hash": mock_tx_hash
        }

    def get_inventory(self, address: str) -> List[Dict[str, Any]]:
        """
        Retrieves a list of all NFTs owned by a given Minima address.
        
        Args:
            address: The Minima address to check.
        
        Returns:
            A list of dictionaries, where each dictionary represents an NFT.
        """
        print(f"Fetching NFT inventory for address: {address}")
        
        # This would call the Minima node's 'tokens' or similar endpoint.
        # We simulate a response with two NFTs for this example.
        mock_inventory = [
            {
                "tokenid": "0x1234567890abcdef" * 4,
                "name": "PrimalsGenesis",
                "description": "The first NFT of the Primals collection.",
                "total_supply": 1,
                "token_decimals": 0
            },
            {
                "tokenid": "0xabcdef1234567890" * 4,
                "name": "PrimalsQuest",
                "description": "An NFT awarded for completing a quest.",
                "total_supply": 1,
                "token_decimals": 0
            }
        ]
        
        return mock_inventory

# --- Example Usage ---
if __name__ == '__main__':
    MINIMA_NODE_API = "http://localhost:9002/api"  # Placeholder URL
    
    nft_module = MinimaNFTModule(MINIMA_NODE_API)

    # Example 1: Minting an NFT
    print("\n--- Minting a new NFT ---")
    new_nft = nft_module.mint_nft(
        "Mx1234...", 
        "PrimalsAlpha", 
        "A special NFT for the first supporters."
    )
    print("Mint Result:", new_nft)

    # Example 2: Getting a user's NFT inventory
    print("\n--- Getting user's inventory ---")
    user_nfts = nft_module.get_inventory("Mx5678...")
    print("User NFTs:", user_nfts)

    # Example 3: Transferring an NFT
    print("\n--- Transferring an NFT ---")
    transfer_result = nft_module.transfer_nft(
        "Mx1234...", 
        "Mx5678...", 
        "0x1234567890abcdef" * 4
    )
    print("Transfer Result:", transfer_result)
        
