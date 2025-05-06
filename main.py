from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
from eth_account import Account
from hyperliquid.exchange import Exchange

# Load environment variables
load_dotenv()

PRIVATE_KEY = os.getenv("PRIVATE_KEY")
if not PRIVATE_KEY:
    raise ValueError("PRIVATE_KEY not set in environment")

wallet = Account.from_key(PRIVATE_KEY)
exchange = Exchange(wallet=wallet)

app = Flask(__name__)

@app.route("/")
def index():
    return "Bot is running!"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    symbol = data.get("symbol", "")
    size = float(data.get("size", 1))
    action = data.get("action", "buy").lower()

    try:
        if action == "buy":
            resp = exchange.market_open(symbol, is_buy=True, sz=size)
        elif action == "sell":
            resp = exchange.market_open(symbol, is_buy=False, sz=size)
        else:
            return jsonify({"error": "Invalid action"}), 400
        return jsonify(resp), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
