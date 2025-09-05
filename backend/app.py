from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import json
import firebase_admin
from firebase_admin import credentials, firestore

# --- Firebase Configuration (Provided by Canvas) ---
__firebase_config = '{}'
__app_id = 'your-app-id'

# Use this path for public collections, as defined by Firestore security rules.
PUBLIC_COLLECTION_PATH = f"artifacts/{__app_id}/public/data"

# --- Firebase Initialization ---
try:
    firebase_config = json.loads(__firebase_config)
    cred = credentials.Certificate(firebase_config)
    firebase_admin.initialize_app(cred)
    print("Firebase initialized successfully.")
except (json.JSONDecodeError, ValueError, KeyError, Exception) as e:
    print(f"Failed to initialize Firebase: {e}")

db = firestore.client()

# --- Core Modules (including new DEX class) ---
from minima_wallet import MinimaWallet
from minima_nft_marketplace import NFTMarketplace
from minima_bridge import MinimaBridge
from custom_token import CustomToken

class FirestoreDEX:
    """
    Manages DEX data (reserves, liquidity) using Firestore.
    """
    def __init__(self, db_client):
        self.db = db_client
        self.reserves_ref = self.db.collection(PUBLIC_COLLECTION_PATH).document('dex').collection('reserves')

    def update_reserves(self, token_a, token_b, reserve_a, reserve_b):
        """
        Updates the reserves for a token pair in Firestore.
        In a real application, this would be triggered by a contract event.
        """
        try:
            doc_ref = self.reserves_ref.document(f"{token_a}-{token_b}")
            doc_ref.set({
                "token_a": token_a,
                "token_b": token_b,
                "reserve_a": reserve_a,
                "reserve_b": reserve_b,
                "updatedAt": firestore.SERVER_TIMESTAMP
            })
            print(f"Reserves for {token_a}-{token_b} updated in Firestore.")
        except Exception as e:
            print(f"Failed to update DEX reserves: {e}")

    def get_reserves(self, token_a, token_b):
        """
        Retrieves the latest reserves for a token pair.
        """
        try:
            doc_ref = self.reserves_ref.document(f"{token_a}-{token_b}")
            doc = doc_ref.get()
            if doc.exists:
                return doc.to_dict()
            else:
                return {"error": "Reserves not found for this token pair."}
        except Exception as e:
            print(f"Failed to get DEX reserves: {e}")
            return {"error": "Failed to fetch reserves from database."}

# Initialize Flask and all core modules with the Firestore client
app = Flask(__name__)
CORS(app)
wallet = MinimaWallet()
marketplace = NFTMarketplace()
bridge = MinimaBridge()
token = CustomToken()
dex = FirestoreDEX(db)

# --- WALLET ENDPOINTS (unchanged) ---
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

# --- NEW: DEX API ENDPOINTS ---
@app.route('/api/dex/reserves', methods=['GET'])
def get_dex_reserves():
    """
    Returns the current reserves for a token pair from Firestore.
    Requires 'token_a' and 'token_b' query parameters.
    """
    token_a = request.args.get('token_a')
    token_b = request.args.get('token_b')
    if not token_a or not token_b:
        return jsonify({"error": "Missing token_a or token_b query parameter"}), 400
    
    reserves = dex.get_reserves(token_a, token_b)
    if reserves:
        return jsonify({"reserves": reserves})
    return jsonify({"error": "Failed to fetch reserves"}), 500

@app.route('/api/dex/update-reserves', methods=['POST'])
def update_dex_reserves():
    """
    Endpoint to manually update reserves (for testing).
    In a real app, this would be an internal function or triggered by a webhook.
    """
    data = request.get_json()
    token_a = data.get('token_a')
    token_b = data.get('token_b')
    reserve_a = data.get('reserve_a')
    reserve_b = data.get('reserve_b')
    
    if not all([token_a, token_b, reserve_a, reserve_b]):
        return jsonify({"error": "Missing required parameters"}), 400

    dex.update_reserves(token_a, token_b, reserve_a, reserve_b)
    return jsonify({"message": "Reserves updated successfully"}), 200


if __name__ == '__main__':
    # This is a placeholder. A real deployment would use a production-ready server.
    app.run(debug=True, port=5000)
