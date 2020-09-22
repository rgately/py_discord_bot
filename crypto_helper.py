import json, hmac, hashlib, time, requests, base64
from requests.auth import AuthBase
import json


API_KEY = None
PASSPHRASE = None
SECRET = None

with open("keys.json") as keys :
    keys_json = json.load(keys)
    API_KEY = keys_json["coinbase_api_key"]
    PASSPHRASE = keys_json["coinbase_passphrase"]
    SECRET = keys_json["coinbase_secret"]


supported_currencies = {"xrp" : "XRP-USD", "eth" : "ETH-USD", "btc" : "BTC-USD"}

class CoinbaseAuth(AuthBase) :

    def __init__(self, api_key, secret_key, passphrase) :
        self.api_key = api_key
        self.secret_key = secret_key
        self.passphrase = passphrase

    def __call__(self, request) :
        timestamp = str(time.time())
        message = str(timestamp + str(request.method) + str(request.path_url) + str((request.body or '')))
        hmac_key = base64.b64decode(self.secret_key)
        signature = hmac.new(hmac_key, msg=message.encode('utf-8'), digestmod=hashlib.sha256)
        signature_b64 = base64.b64encode(signature.digest())
        #signature_b64 = signature.digest().encode('base64').rstrip('\n')

        request.headers.update({
            'CB-ACCESS-SIGN': signature_b64,
            'CB-ACCESS-TIMESTAMP': timestamp,
            'CB-ACCESS-KEY': self.api_key,
            'CB-ACCESS-PASSPHRASE': self.passphrase,
            'Content-Type': 'application/json'
        })

        return request



def get_price(currency) :

    currency = currency.strip()
    if (currency.lower() in supported_currencies.keys()) :
        currency = supported_currencies[currency.lower()]
    elif not currency in supported_currencies.values() :
        return -1

    auth = CoinbaseAuth(str(API_KEY), str(SECRET), str(PASSPHRASE))

    price_data = requests.get("https://api.pro.coinbase.com/products/" + currency + "/ticker", auth=auth)
    price_json = price_data.json()
    return price_json["price"]
