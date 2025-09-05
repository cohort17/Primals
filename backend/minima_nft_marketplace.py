import json

class NFTMarketplace:
    """
    A class to simulate the backend logic of an NFT marketplace.
    This module handles listing, bidding, and selling NFTs.
    It works with a simple in-memory state for demonstration.
    """

    def __init__(self):
        self.listings = {}
        self.bids = {}
        self.next_listing_id = 1

    def list_nft_for_sale(self, token_id, owner_address, price):
        """
        Simulates listing an NFT on the marketplace.
        
        Args:
            token_id (str): The ID of the NFT to list.
            owner_address (str): The address of the NFT owner.
            price (float): The list price of the NFT.

        Returns:
            dict: The new listing details or None if listing fails.
        """
        if token_id in self.listings:
            print(f"Error: NFT with ID {token_id} is already listed.")
            return None
        
        listing_id = f"LST_{self.next_listing_id}"
        self.next_listing_id += 1
        
        self.listings[listing_id] = {
            "token_id": token_id,
            "owner": owner_address,
            "price": price,
            "status": "for_sale",
            "bids": []
        }
        print(f"NFT {token_id} successfully listed by {owner_address} for {price} MINIMA.")
        return self.listings[listing_id]

    def place_bid(self, listing_id, bidder_address, bid_amount):
        """
        Simulates a user placing a bid on a listed NFT.

        Args:
            listing_id (str): The ID of the listing.
            bidder_address (str): The address of the bidder.
            bid_amount (float): The amount of the bid.

        Returns:
            bool: True if the bid was successful, False otherwise.
        """
        if listing_id not in self.listings or self.listings[listing_id]['status'] != 'for_sale':
            print(f"Error: Listing {listing_id} not found or not for sale.")
            return False

        listing = self.listings[listing_id]
        new_bid = {
            "bidder": bidder_address,
            "amount": bid_amount
        }
        listing['bids'].append(new_bid)
        print(f"Bid of {bid_amount} MINIMA placed on listing {listing_id} by {bidder_address}.")
        return True

    def accept_highest_bid(self, listing_id, owner_address):
        """
        Simulates a seller accepting the highest bid.

        Args:
            listing_id (str): The ID of the listing.
            owner_address (str): The address of the listing owner.

        Returns:
            bool: True if the sale was successful, False otherwise.
        """
        if listing_id not in self.listings or self.listings[listing_id]['owner'] != owner_address:
            print("Error: Invalid listing ID or not the owner.")
            return False

        listing = self.listings[listing_id]
        if not listing['bids']:
            print("Error: No bids to accept.")
            return False

        # Find the highest bid
        highest_bid = max(listing['bids'], key=lambda bid: bid['amount'])

        # Simulate the sale and token transfer
        listing['status'] = 'sold'
        print(f"Sale successful! NFT {listing['token_id']} sold to {highest_bid['bidder']} for {highest_bid['amount']} MINIMA.")

        # Simulate clearing the bids for this listing
        listing['bids'] = []

        return True

    def get_all_listings(self):
        """Returns all current listings on the marketplace."""
        return self.listings

if __name__ == '__main__':
    marketplace = NFTMarketplace()
    
    owner = "MxOwner123"
    bidder_A = "MxBidderA456"
    bidder_B = "MxBidderB789"
    nft_id = "NFT001"
    
    print("--- STEP 1: Listing an NFT ---")
    listing = marketplace.list_nft_for_sale(nft_id, owner, 10.0)
    print("\n")
    
    print("--- STEP 2: Placing Bids ---")
    marketplace.place_bid(list(marketplace.get_all_listings().keys())[0], bidder_A, 11.5)
    marketplace.place_bid(list(marketplace.get_all_listings().keys())[0], bidder_B, 12.0)
    print("\n")
    
    print("--- STEP 3: Accepting the Highest Bid ---")
    marketplace.accept_highest_bid(list(marketplace.get_all_listings().keys())[0], owner)
    print("\n")
    
    print("--- Final Listings State ---")
    print(json.dumps(marketplace.get_all_listings(), indent=2))
      
