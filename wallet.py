import flask
import random
import string
from sqlalchemy import exc
from extensions import db
from flask_login import login_required, current_user
from models import WalletInfo, CryptoCoin, TronInfo
from forms import WalletValidator, WalletTransactions, InputTransaction, TronMoney, CashForm
from crypto_container import burning_action
from dashboard_table import current_tron_price
from tron_crypto import address_validator, send_tron
from auth import submit_verification, totp
wallet = flask.Blueprint("wallet", __name__, template_folder="templates")

def global_exist(instance_one, instance_two):
    if db.session.query(db.exists().where(instance_one == instance_two)).scalar() == True:
        return True 
    else:
        return False
   
@wallet.route("/create_wallet", methods=["GET", "POST"])
@login_required
def create_wallet():
    wallet_form = WalletValidator()
    if wallet_form.validate_on_submit():
        if global_exist(WalletInfo.wallet_name, wallet_form.data.data) == False:
            unique_id = random.randint(100000, 999999)
            string_key = "".join(random.choice(string.ascii_lowercase) for i in range(30))
            balance = 0.0
            unique_username = current_user.username
            try: 
                db.session.add(WalletInfo(unique_id, string_key, wallet_form.data.data, 
                                          balance, unique_username))
                db.session.commit()
                flask.flash("You already have created your wallet!", category="success")
            except exc.IntegrityError:
                db.session.rollback()
        else:
            flask.flash("Invalid input", category = "error")
    return flask.render_template("create_wallet.html", wallet_form=wallet_form)
            

@wallet.route("/get_wallet", methods=["GET", "POST"])
@login_required
def get_wallet():
    wallet_form = WalletValidator()
    if wallet_form.validate_on_submit():
        if global_exist(WalletInfo.wallet_name, wallet_form.data.data) == True:
            wallet_data = WalletInfo.query.filter_by(wallet_name = wallet_form.data.data).first()
            if wallet_data.unique_username == current_user.username:
                wallet_list = [wallet_data.wallet_id,
                               wallet_data.wallet_key,
                               wallet_data.wallet_name,
                               wallet_data.wallet_balance]
                return flask.render_template("get_wallet.html", wallet_form=wallet_form, wallet_list=wallet_list)
            else:
                flask.flash("No access", category = "error")
        else:
            flask.flash("Invalid input", category = "error")

    return flask.render_template("get_wallet.html", wallet_form=wallet_form)

@wallet.route("/wallet_transactions", methods=["GET", "POST"])
@login_required 
def wallet_transactions():
    form_trans = WalletTransactions()
    if form_trans.validate_on_submit():
        if global_exist(WalletInfo.wallet_key, form_trans.key_data.data) == True:
            form_data = WalletInfo.query.filter_by(wallet_key = form_trans.key_data.data).first()
            if form_data.unique_username == current_user.username and \
            global_exist(form_data.wallet_id, WalletInfo.wallet_id) and \
            global_exist(form_trans.receiver.data, WalletInfo.wallet_name) == True:
                    if form_trans.sum_data.data < 0.0:
                        flask.flash("Invalid money input", category = "error")
                    elif form_data.wallet_balance < form_trans.sum_data.data:
                        flask.flash("No money", category = "error")
                    else:
                        form_data.wallet_balance = form_data.wallet_balance - form_trans.sum_data.data
                        receiver_data = WalletInfo.query.filter_by(wallet_name = form_trans.receiver.data).first()
                        receiver_data.wallet_balance = receiver_data.wallet_balance + form_trans.sum_data.data
                        try:
                            db.session.commit()
                        except:
                            db.session.rollback()
                        flask.flash("Success!", category="success")
                        return flask.render_template("transactions_wallet.html", form_trans=form_trans)
            else:
                flask.flash("Invalid input", category = "error")
    return flask.render_template("transactions_wallet.html" , form_trans=form_trans)        
    
@wallet.route("/replenishment", methods=['GET', 'POST'])
@login_required   
def replenishment():
    form_trans = InputTransaction()
    if form_trans.validate_on_submit():
        if global_exist(WalletInfo.wallet_key, form_trans.key_data.data) == True:
            form_data = WalletInfo.query.filter_by(wallet_key = form_trans.key_data.data).first() 
            get_crypto = CryptoCoin.query.filter_by(storage_auth = "protect").first()
            access_to_tron = TronInfo.query.filter_by(current_username = current_user.username).first()
            if form_trans.sum_data.data < 0.0 or form_trans.sum_data.data > get_crypto.crypto_storage or form_trans.sum_data.data > access_to_tron.tron_amount:
               flask.flash("Invalid money input", category = "error")
            else:
                get_crypto.crypto_storage = get_crypto.crypto_storage - form_trans.sum_data.data
                form_data.wallet_balance = form_data.wallet_balance + form_trans.sum_data.data
                access_to_tron.tron_amount = access_to_tron.tron_amount - form_trans.sum_data.data
                try:
                    db.session.commit()
                except:
                    db.session.rollback()
                burning_action()
                flask.flash("Success!", category="success")
                return flask.render_template("replenishment.html" , form_trans=form_trans)
        else:
            flask.flash("Invalid input", category = "error")
    return flask.render_template("replenishment.html" , form_trans=form_trans) 
   
@wallet.route("/get_balance_menu", methods=["GET", "POST"])     
@login_required
def get_balance_menu():
    form_tron = TronMoney()
    if form_tron.validate_on_submit():
        access_to_crypto = CryptoCoin.query.filter_by(storage_auth = "protect").first()
        access_to_tron = TronInfo.query.filter_by(current_username = current_user.username).first()
        crypto_price = access_to_crypto.dollar_price
        if address_validator(form_tron.tron_wallet_form.data) == True:
            if form_tron.amount.data > 0:
                final_tron = (form_tron.amount.data * float(current_tron_price())) / crypto_price
                access_to_tron.tron_amount = final_tron + access_to_tron.tron_amount
                try:
                    send_tron(form_tron.amount.data, form_tron.tron_wallet_form.data)
                except Exception as e:
                    return e
                try:
                    db.session.commit()
                except:
                    db.session.rollback()
            else:
                flask.flash("Invalid money input", category = "error")
            flask.flash("Success!", category="success")
            return flask.render_template("tron_transactions.html", form_tron=form_tron)
        else:
            flask.flash("Invalid address input", category = "error")
    return flask.render_template("tron_transactions.html", form_tron=form_tron)

@wallet.route("/get_to_cash", methods=["GET", "POST"])
@login_required
def get_to_cash():
    cash_form = CashForm()
    if cash_form.validate_on_submit():
        if global_exist(WalletInfo.wallet_key, cash_form.key_data.data) == True:
            form_data = WalletInfo.query.filter_by(wallet_key = cash_form.key_data.data).first()
            if form_data.wallet_id == cash_form.commit_id.data:
                if cash_form.sum_data.data > form_data.wallet_balance or cash_form.sum_data.data < 0.0:
                    flask.flash("Invalid money input", category = "error")
                else:
                    access_to_crypto = CryptoCoin.query.filter_by(storage_auth = "protect").first()
                    form_data.wallet_balance = form_data.wallet_balance - cash_form.sum_data.data
                    you_will_have = float(access_to_crypto.dollar_price * cash_form.sum_data.data)
                    if totp.verify(cash_form.two_factor_auth.data) == True:
                        try:
                            db.session.commit()
                        except:
                            db.session.rollback()        
                        flask.flash(f"You will have {you_will_have}", category="success")
                        return flask.render_template("cash_transactions.html", cash_form=cash_form, submit_verification=submit_verification)
                    else:
                        flask.flash("Incorrect submit password", category="error")
            else:
                flask.flash("Error with wallet_id", category="error")
        else:
            flask.flash("Error with crypto_key", category="error")
    return flask.render_template("cash_transactions.html", cash_form=cash_form, submit_verification=submit_verification)                
    
@wallet.before_request
def database_tron_connection():
    if flask.request.path == '/wallet/dashboard':
        try:
            unique_username = current_user.username
            db.session.add(TronInfo(unique_username, 0.0))
            db.session.commit()
        except:
            db.session.rollback()
        
    
@wallet.route("/dashboard", methods=['GET', 'POST'])
@login_required
def dashboard():
    return flask.render_template("dashboard.html")




   
 