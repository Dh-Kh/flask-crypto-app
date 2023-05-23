from extensions import db
from models import CryptoCoin, WalletInfo
import flask
crypto_container = flask.Blueprint("crypto_container", __name__, template_folder="templates")

@crypto_container.before_app_first_request
def burning_start():
    if db.session.query(CryptoCoin).first() == None:
        storage_value = 100000000
        storage_auth = "protect"
        dollar_value = 0.0
    try:
        db.session.add(CryptoCoin(storage_value, storage_auth, dollar_value))
        db.session.commit()
    except:
        db.session.rollback()
        
@crypto_container.before_app_request
def define_current_price():
    access_to_crypto = CryptoCoin.query.filter_by(storage_auth = "protect").first()
    crypto_price = access_to_crypto.crypto_storage
    money_in_wallet = WalletInfo.query.with_entities(WalletInfo.wallet_balance).all()   
    current_price = sum(balance[0] for balance in money_in_wallet) / crypto_price
    access_to_crypto.dollar_price = current_price
    try:
        db.session.commit()
    except:
        db.session.rollback()
    


def burning_action():
    out = 100
    access_to_crypto = CryptoCoin.query.filter_by(storage_auth = "protect").first()
    access_to_crypto.crypto_storage = (access_to_crypto.crypto_storage - out)
    try:
        db.session.commit()
    except:
        db.session.rollback()
    
def do_task_acction():
    pass
    
    
   

    

