from flask_login import UserMixin
from extensions import db

class UserInfo(UserMixin, db.Model):
    __tablename__ = "user_info"
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(100), unique = True)
    password = db.Column(db.String(100))
    def __init__(self, username, password):
       self.username = username
       self.password = password
    
    def is_active(self):
        return True
   
    def is_authenticated(self):
       return self.id is not None
    
    def is_anonymous(self):
        return False
    
    def get_id(self):
        return str(self.id)
    
class WalletInfo(db.Model):
    __tablename__ = "wallet_info"
    wallet_id = db.Column(db.Integer, unique = True, primary_key = True)
    wallet_key = db.Column(db.String(100), unique = True)
    wallet_name = db.Column(db.String(100), unique = True)
    wallet_balance = db.Column(db.Float)
    unique_username = db.Column(db.String(100))
    def __init__(self, wallet_id, wallet_key, wallet_name, wallet_balance, unique_username):
         self.wallet_id = wallet_id
         self.wallet_key = wallet_key
         self.wallet_name = wallet_name
         self.wallet_balance = wallet_balance
         self.unique_username = unique_username

class CryptoCoin(db.Model):
    __tablename__ = "crypto_coin"
    crypto_id = db.Column(db.Integer, primary_key = True)
    crypto_storage = db.Column(db.Float)
    storage_auth = db.Column(db.String(100))
    dollar_price = db.Column(db.Float)
    def __init__(self, crypto_storage, storage_auth, dollar_price):
        self.crypto_storage = crypto_storage
        self.storage_auth = storage_auth
        self.dollar_price = dollar_price
        
class TronInfo(db.Model):
    __tablename__ = "tron_info"
    table_id = db.Column(db.Integer, primary_key = True)
    current_username = db.Column(db.String(100), unique = True)
    tron_amount = db.Column(db.Float)
    def __init__(self, current_username, tron_amount):
        self.current_username = current_username
        self.tron_amount = tron_amount