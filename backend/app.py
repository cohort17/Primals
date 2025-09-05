from flask import Flask, jsonify, request
import os
import firebase_admin
from firebase_admin import credentials, firestore

# --- Firebase Configuration (Provided by Canvas) ---
# NOTE: In a real environment, these would be loaded from environment variables.
# The `__firebase_config` variable is provided by the canvas environment.
__firebase_config = '{}'
# The `__app_id` variable is provided by the canvas environment.
__app_id = 'your-app-id'

# Use this path for public collections, as defined by Firestore security rules.
# This ensures data is accessible to anyone.
PUBLIC_COLLECTION_PATH = f"artifacts/{__app_id}/public/data"

# --- Firebase Initialization ---
try:
    firebase_config = json.loads(__firebase_config)
    # The `firebase-admin` library needs a service account credential.
    # For local development, you would set the GOOGLE_APPLICATION_CREDENTIALS
    # environment variable.
    # Here, we will try to initialize with the provided config.
    cred = credentials.Certificate(firebase_config)
    firebase_admin.initialize_app(cred)
    print("Firebase initialized successfully.")
except (json.JSONDecodeError, ValueError, KeyError, Exception) as e:
    print(f"Failed to initialize Firebase: {e}")
    # In a real application, you might exit or handle this error more gracefully.

db = firestore.client()

# Import other modules
# These now need to be modified to accept a Firestore client
from minima_wallet import MinimaWallet
from minima_bridge import MinimaBridge
# from minima_nft_marketplace import NFTMarketplace # We will replace this with a Firestore-based class

class FirestoreNFTMarketplace:
    """
    Manages NFT listings using a Firestore database for persistent storage.
    """
    def __init__(self, db_client):
        self.db = db_client
        self.listings_ref = self.db.collection(PUBLIC_COLLECTION_PATH).document('marketplace').collection('listings')

    def list_nft_for_sale(self, token_id, owner_address, price):
        """
        Creates a new NFT listing document in Firestore.
        """
        try:
            new_listing_ref = self.listings_ref.document()
            listing_data = {
                "token_id": token_id,
                "owner_address": owner_address,
                "price": price,
                "status": "for_sale",
                "createdAt": firestore.SERVER_TIMESTAMP
            }
            new_listing_ref.set(listing_data)
            print(f"NFT {token_id} listed for sale in Firestore.")
            return {"id": new_listing_ref.id, **listing_data}
        except Exception as e:
            print(f"Failed to list NFT in Firestore: {e}")
            return None

    def get_all_listings(self):
        """
        Retrieves all active NFT listings from Firestore.
        """
        try:
            listings = []
            docs = self.listings_ref.stream()
            for doc in docs:
                data = doc.to_dict()
                listings.append({"id": doc.id, **data})
            return listings
        except Exception as e:
            print(f"Failed to retrieve listings from Firestore: {e}")
            return []

# Initialize Flask and our core modules with the Firestore client
app = Flask(__name__)
wallet = MinimaWallet()
marketplace = FirestoreNFTMarketplace(db)

# WALLET ENDPOINTS (remain unchanged from before)
# -----------------------------------------------------------------------------
@app.route('/api/wallet/balance', methods=['GET'])
def get_wallet_balance():
    token_id = request.args.get('token_id', '0x00')
    balance = wallet.get_balance(token_id)
    if balance:
        return jsonify(balance)
    return jsonify({"error": "Failed to retrieve balance"}), 500

@app.route('/api/wallet/send', methods=['POST'])
def send_transaction():
    data = request.get_json()
    recipient = data.get('recipient_address')
    amount = data.get('amount')
    token_id = data.get('token_id', '0x00')
    if not all([recipient, amount]):
        return jsonify({"error": "Missing recipient or amount"}), 400
    result = wallet.send_transaction(recipient, amount, token_id)
    if result:
        return jsonify(result)
    return jsonify({"error": "Transaction failed"}), 500

# NEW: FIRESTORE-INTEGRATED MARKETPLACE ENDPOINTS
# -----------------------------------------------------------------------------
@app.route('/api/marketplace/listings', methods=['GET'])
def get_all_listings():
    """Returns a list of all current NFT listings from Firestore."""
    listings = marketplace.get_all_listings()
    return jsonify({"listings": listings})

@app.route('/api/marketplace/list-nft', methods=['POST'])
def list_nft():
    """
    Lists an NFT for sale by adding it to Firestore.
    Requires 'token_id', 'owner_address', and 'price' in the JSON body.
    """
    data = request.get_json()
    token_id = data.get('token_id')
    owner_address = data.get('owner_address')
    price = data.get('price')
    
    if not all([token_id, owner_address, price]):
        return jsonify({"error": "Missing required parameters"}), 400
        
    listing = marketplace.list_nft_for_sale(token_id, owner_address, price)
    if listing:
        return jsonify(listing), 201
    return jsonify({"error": "Failed to list NFT"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
