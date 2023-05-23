from tronpy import Tron
from tronpy.providers import HTTPProvider
from tronpy.keys import PrivateKey
import os
from pathlib import Path
from dotenv import load_dotenv
basepath = Path()
basedir = str(basepath.cwd())
envars = basepath.cwd() / '.env'
load_dotenv(envars)
HALF_TRON = 500000
ONE_TRON = 1000000
wallet_tron = os.getenv("WALLET_TRON")
tron_key = os.getenv("TRON_KEY")
http_provider = HTTPProvider(endpoint_uri=os.getenv("ENDPOINT_URI"), api_key=os.getenv("API_KEY"))
client = Tron(provider=http_provider)

def address_validator(address):
    try:
        return client.is_address(address)
    except ValueError as v:
        return v

def send_tron(amount, wallet):
    try:
        priv_key = PrivateKey(bytes.fromhex(tron_key))
        txn = (
            client.trx.transfer(wallet_tron, str(wallet), int(amount))
            .memo("Transaction Description")
            .build()
            .inspect()
            .sign(priv_key)
            .broadcast()
            )
        return txn.wait()

    except Exception as e:
        return e

def tron_balance(wallet):
    return client.get_account_balance(wallet)


