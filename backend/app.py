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

# Import other modules
from minima_wallet import MinimaWallet
from minima_nft_marketplace import NFTMarketplace
# We will use our own Firestore-integrated bridge class

class FirestoreMinimaBridge:
    """
    Manages bridge transactions using a Firestore database for persistent storage.
    """
    def __init__(self, db_client):
        self.db = db_client
        self.transactions_ref = self.db.collection(PUBLIC_COLLECTION_PATH).document('bridge').collection('transactions')

    def start_bridging_process(self, token_id, amount, evm_address):
        """
        Simulates the start of a bridge process and saves it to Firestore.
        """
        try:
            new_tx_ref = self.transactions_ref.document()
            tx_data = {
                "token_id": token_id,
                "amount": amount,
                "evm_address": evm_address,
                "status": "pending",
                "createdAt": firestore.SERVER_TIMESTAMP,
                "transactionId": new_tx_ref.id
            }
            new_tx_ref.set(tx_data)
            print(f"Bridge transaction for {amount} of {token_id} initiated and saved to Firestore.")
            return tx_data
        except Exception as e:
            print(f"Failed to start bridge transaction: {e}")
            return None

    def get_transaction_status(self, transaction_id):
        """
        Retrieves the status of a bridge transaction from Firestore.
        """
        try:
            doc_ref = self.transactions_ref.document(transaction_id)
            doc = doc_ref.get()
            if doc.exists:
                return {"id": doc.id, **doc.to_dict()}
            else:
                return None
        except Exception as e:
            print(f"Failed to retrieve transaction status: {e}")
            return None

# Initialize Flask and our core modules with the Firestore client
app = Flask(__name__)
CORS(app)
wallet = MinimaWallet()
marketplace = NFTMarketplace()
bridge = FirestoreMinimaBridge(db) # Use the new Firestore-based bridge class

# WALLET ENDPOINTS (unchanged)
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

# NEW: FIRESTORE-INTEGRATED BRIDGE ENDPOINTS
# -----------------------------------------------------------------------------
@app.route('/api/bridge/start', methods=['POST'])
def start_bridge_process():
    """
    Initiates the cross-chain bridging process and logs it to Firestore.
    Requires a JSON body with 'token_id', 'amount', and 'evm_address'.
    """
    data = request.get_json()
    token_id = data.get('token_id')
    amount = data.get('amount')
    evm_address = data.get('evm_address')
    if not all([token_id, amount, evm_address]):
        return jsonify({"error": "Missing required parameters"}), 400
    result = bridge.start_bridging_process(token_id, amount, evm_address)
    if result:
        return jsonify({"message": "Bridge process initiated", "transaction": result}), 201
    return jsonify({"error": "Failed to start bridging process"}), 500

@app.route('/api/bridge/status/<string:transaction_id>', methods=['GET'])
def get_bridge_status(transaction_id):
    """
    Returns the current status of a bridge transaction from Firestore.
    """
    status = bridge.get_transaction_status(transaction_id)
    if status:
        return jsonify({"status": status})
    return jsonify({"error": "Transaction not found"}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)
