from flask import Flask, jsonify, request
# We'll need to install Flask with `pip install Flask`.
# We also need to install requests with `pip install requests`.

# Assuming all your modules are in the same directory, import them
# In a real-world scenario, you would structure your project with a `src` folder
# and handle imports more formally, but this works for our current structure.
from minima_wallet import MinimaWallet
from minima_bridge import MinimaBridge
from minima_nft_marketplace import NFTMarketplace

# Initialize the Flask application
app = Flask(__name__)

# Initialize our core module classes
# These can be considered singletons for our simple API
wallet = MinimaWallet()
bridge = MinimaBridge()
marketplace = NFTMarketplace()

# Endpoint for the home page or a simple status check
@app.route('/')
def home():
    """A simple status endpoint to confirm the API is running."""
    return jsonify({
        "status": "online",
        "message": "Welcome to the Primals DApp Backend API."
    })

# WALLET ENDPOINTS
# -----------------------------------------------------------------------------
@app.route('/api/wallet/balance', methods=['GET'])
def get_wallet_balance():
    """
    Returns the balance of the wallet for a given token.
    Example: GET /api/wallet/balance?token_id=0x00
    """
    token_id = request.args.get('token_id', '0x00')
    balance = wallet.get_balance(token_id)
    if balance:
        return jsonify(balance)
    return jsonify({"error": "Failed to retrieve balance"}), 500

@app.route('/api/wallet/send', methods=['POST'])
def send_transaction():
    """
    Sends a transaction from the wallet.
    Requires a JSON body with 'recipient', 'amount', and 'token_id'.
    """
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

# BRIDGE ENDPOINTS
# -----------------------------------------------------------------------------
@app.route('/api/bridge/start', methods=['POST'])
def start_bridge_process():
    """
    Initiates the cross-chain bridging process.
    Requires a JSON body with 'token_id', 'amount', and 'evm_address'.
    """
    data = request.get_json()
    token_id = data.get('token_id')
    amount = data.get('amount')
    evm_address = data.get('evm_address')

    if not all([token_id, amount, evm_address]):
        return jsonify({"error": "Missing required parameters"}), 400

    # Simulate calling the bridge's main function
    result = bridge.start_bridging_process(token_id, amount, evm_address)
    if result:
        return jsonify({"message": "Bridge process initiated", "transaction_id": result['transaction_id']})
    return jsonify({"error": "Failed to start bridging process"}), 500

# NFT MARKETPLACE ENDPOINTS
# -----------------------------------------------------------------------------
@app.route('/api/marketplace/listings', methods=['GET'])
def get_all_listings():
    """Returns a list of all current NFT listings."""
    listings = marketplace.get_all_listings()
    return jsonify({"listings": listings})

@app.route('/api/marketplace/list-nft', methods=['POST'])
def list_nft():
    """
    Lists an NFT for sale on the marketplace.
    Requires 'token_id', 'owner_address', and 'price'.
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
    # Start the Flask development server
    # The `debug=True` is great for development, but should be set to False in production.
    app.run(debug=True, port=5000)
