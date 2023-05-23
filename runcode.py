import flask
from extensions import db
from datetime import timedelta
from wallet import wallet
from crypto_container import crypto_container
from auth import auth, login_manager, mail_sender
from dashboard_table import dashboard_table
import os
from pathlib import Path
from dotenv import load_dotenv
basepath = Path()
basedir = str(basepath.cwd())
envars = basepath.cwd() / '.env'
load_dotenv(envars)
app = flask.Flask(__name__, template_folder="templates")
app.secret_key = os.getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["USE_SESSION_FOR_NEXT"] = True
app.config['SQLALCHEMY_POOL_SIZE'] = 10
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(hours=2)
app.config["REMEMBER_COOKIE_DURATION"] = timedelta(days=30)
app.config.update(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 465,
    MAIL_USE_SSL = True,
    MAIL_USE_TLS = False,
    MAIL_USERNAME = os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    )

with app.app_context():
    app.register_blueprint(auth)
    app.register_blueprint(wallet, url_prefix = "/wallet")
    app.register_blueprint(crypto_container, url_prefix = "/crypto_container")
    app.register_blueprint(dashboard_table)
    db.init_app(app)
    login_manager.init_app(app)
    mail_sender.init_app(app)
    db.create_all()

    
if __name__ == "__main__":
    app.run(debug=True)





       

       

       
