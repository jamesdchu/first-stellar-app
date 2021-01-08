import os, requests, json, stellar_sdk, urllib.parse
from flask import Flask, render_template, request, session
from flask_session import Session
from stellar_sdk import Server, Asset, Account, Keypair, TransactionBuilder, Network

# Accounts endpoint - get info about an account.
accounts_url = 'https://horizon-testnet.stellar.org/accounts/{}'
# Interact with test net.
server = Server(horizon_url='https://horizon-testnet.stellar.org')
# URL for path endpoint - find path from x to y.
path_url = 'https://horizon-testnet.stellar.org/paths/strict-send?destination_assets={}%3A{}&source_asset_type=native&source_amount={}'

# Creating an account
def create_account(): 
    pair = Keypair.random()
    print(f"Secret: {pair.secret}")
    print(f"Public Key: {pair.public_key}") 
    public_key = pair.public_key
    secret_key = pair.secret_key
    response = requests.get(f"https://friendbot.stellar.org?addr={public_key}")
    if response.status_code == 200:
        print(f"SUCCESS! You have a new account :)\n{response.text}")
    else:
        print(f"ERROR! Response: \n{response.text}")

def balance(): 
    server = Server("https://horizon-testnet.stellar.org")
    public_key = "GD4NB2FLQAN5JO7PKPGZJMNBDYQXVSNVC7DEIZMOL5WSNSBLEBUTEF5Q" #SUBSTITUTE WITH MONGODB INFO
    account = server.accounts().account_id(public_key).call()
    for balance in account['balances']:
        print(f"Type: {balance['asset_type']}, Balance: {balance['balance']}")

def create_app(test_config=None):
    # Create and configure the Flask app.
    app = Flask(__name__, instance_relative_config=True)
    app.secret_key = 'super secret key' # obv don't use this in prod

    # Home page
    @app.route('/')
    def index():
        return render_template('index.html')

    # Show balances and enter trade details
    @app.route('/account', methods=('GET', 'POST'))
    def account():
        # If user enters public key, grab and store it, otherwise get pub key from session.
        if 'pubkey' in request.form:
            pub_key =  request.form['pubkey']
            session['pub_key'] = pub_key
        else:
            pub_key = session.get('pub_key', None)

        # Get information from Horizon accounts end point.
        r = requests.get(accounts_url.format(pub_key))
        json_obj = r.json()

        # Store balances in session variable.
        session['balances'] = json_obj
        return render_template('account.html', pub_key=pub_key, json_obj=json_obj)

    # See final trade information, sign & submit transaction
    @app.route('/tx', methods=('GET', 'POST'))
    def transaction():
        # Filled out in Pt. 2 of tutorial. 
        return render_template('tx.html')

    return app
