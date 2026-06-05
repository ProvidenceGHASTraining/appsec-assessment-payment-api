from flask import Flask, request
import sqlite3
import os
import yaml

app = Flask(__name__)

# Demo secrets for assessment only
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET")
PAYMENT_API_TOKEN = os.getenv("PAYMENT_ID")


@app.route("/")
def home():
    return "Payment Review API - Assessment Lab"


@app.route("/payment")
def get_payment():
    username = request.args.get("user")

    conn = sqlite3.connect("payments.db")
    cursor = conn.cursor()

    # Remediated: Parameterized query prevents SQL injection
    query = "SELECT * FROM payments WHERE username = ?"
    cursor.execute(query, (username,))

    result = cursor.fetchall()
    conn.close()

    return str(result)


@app.route("/admin/run")
def admin_run():
    cmd = request.args.get("cmd")
    return os.popen(cmd).read()


@app.route("/account")
def account():
    account_id = request.args.get("id")

    accounts = {
        "1": "Alice Account Balance: 5000",
        "2": "Bob Account Balance: 7500",
        "3": "Admin Account Balance: 99999"
    }

    return accounts.get(account_id, "Account not found")


@app.route("/config/load", methods=["POST"])
def load_config():
    data = request.data.decode("utf-8")

    # Remediated: Safe YAML parsing
    parsed = yaml.safe_load(data)

    return str(parsed)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)