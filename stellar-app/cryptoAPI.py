from stellar_sdk import Server, Asset, Account, Keypair, TransactionBuilder, Network
from stellar_sdk.exceptions import NotFoundError, BadResponseError, BadRequestError

#Verifying Stellar account
def verify_destination(public_key): 
    server = Server("https://horizon-testnet.stellar.org")
    try: 
        server.load_account(public_key)
    except NotFoundError: 
        return False
    return True
        

#Returns all balances in a list --> Can be used to show how much a fundraiser has raised 
def balances(pub_key): 
    server - Server("https://horizon-testnet.stellar.org")
    acount = server.accounts().account_id(public_key).call()
    return acount['balances']

#Sending a payment to a fundraiser
def sendPayment(sender_sKey, destination_pKey, amount, asset_code): 
    server - Server("https://horizon-testnet.stellar.org")
    source_key = Keypair.from_secret(sender_sKey)
    destination_id = destination_pKey

    try: 
        server.load_account(destination_id)
    except NotFoundError: 
        #Shouldn't be a problem since we're using fundraiser wallets (will verify when creating fundraisers/accounts)
        raise Exception("THe destination account is invalid")
    # If there was no error, load up-to-date information on your account.
    source_account = server.load_account(source_key.public_key)
    # Let's fetch base_fee from network
    base_fee = server.fetch_base_fee()
    transaction = (
        TransactionBuilder( 
            source_account=source_account, 
            network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
            base_fee=base_fee
        )
        .append_payment_op(destination=destination_id, amount=str(amount), asset_code=asset_code)
        # .add_text_memo() // COULD ADD DETAILS TO TRANSACTION 
        .set_timeout(10)
        .build()
    )

    #Proof of identity of sender
    transaction.sign(source_key)
    
    try: 
        #Sending the transaction to Stellar
        response = server.submit_transaction(transaction)
        print(f"Response: {response}")
    except (BadRequestError, BadResponseError) as err:
        print(f"Something went wrong!\n{err}")





print(balance(GAMMA7XWCR2FT6OCMT4XNEHAMBMF4IFUUHTXW7N27HWLDDLZ2W74QZPT))











# from requests import Request, Session 
# from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
# import json

# url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
# parameters = {
#   'start':'1',
#   'limit':'5000',
#   'convert':'USD'
# }
# headers = {
#   'Accepts': 'application/json',
#   'X-CMC_PRO_API_KEY': 'c38912a6-bb91-453e-956f-a0a11487a6f4',
# }

# session = Session()
# session.headers.update(headers)

# try:
#   response = session.get(url, params=parameters)
#   data = json.loads(response.text)
#   print(data)
# except (ConnectionError, Timeout, TooManyRedirects) as e:
#   print(e)

