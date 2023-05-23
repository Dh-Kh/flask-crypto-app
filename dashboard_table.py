from bs4 import BeautifulSoup
import flask
import requests
from models import CryptoCoin
import random

dashboard_table = flask.Blueprint("dashboard_table", __name__ , template_folder="templates") 

@dashboard_table.route("/get_stock_prices", methods=["GET", "POST"])
def get_stock_prices():
    response = requests.get("https://coinmarketcap.com/en/currencies/bitcoin/")
    content = response.content
    soup = BeautifulSoup(content, 'html.parser')
    price_table = soup.find("div", {"class": "priceValue"})
    return flask.jsonify(price=price_table.text)

@dashboard_table.route("/get_my_crypto_prices", methods=["GET", "POST"])
def get_my_crypto_prices():
    access_to_crypto = CryptoCoin.query.filter_by(storage_auth = "protect").first()
    return flask.jsonify(crypto = access_to_crypto.dollar_price)

@dashboard_table.route("/chart_data", methods= ["GET", "POST"])
def chart_data():
    random_list = []
    for i in range(7):
        random_data = random.randint(0, 10)
        if len(random_list) == 7:
            random_list.clear()
        else:
            random_list.append(random_data)
    return flask.jsonify(random_list=random_list)

def current_tron_price():
    response = requests.get("https://coinmarketcap.com/en/currencies/tron/")
    content = response.content
    soup = BeautifulSoup(content, 'html.parser')
    price_table = soup.find("div", {"class": "priceValue"})
    return (price_table.text).replace("$", "")