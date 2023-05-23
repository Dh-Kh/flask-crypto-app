import flask
import pyotp
from flask_mail import Mail, Message
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, LoginManager, logout_user, current_user
from extensions import db
from models import UserInfo
from sqlalchemy import exc
from forms import UserForm, CreateUserForm, CheckUserForm, TwoFactor
from ignore_script import DATA1, DATA2
auth = flask.Blueprint("auth", __name__, template_folder="templates")
login_manager = LoginManager()
login_manager.login_view = "connection"
mail_sender = Mail()
totp = pyotp.TOTP("base32secret3232", interval=300)

@login_manager.user_loader
def load_user(id):
    try:
        return UserInfo.query.get(int(id))
    except:
        return None
    
@login_manager.unauthorized_handler
def unauthorized():
    return flask.redirect(flask.url_for("auth.connection"))

def global_exist(instance_one, instance_two):
    if db.session.query(db.exists().where(instance_one == instance_two)).scalar() == True:
        return True 
    else:
        return False
    
@auth.route("/")
def redirection_page():
    if current_user.is_authenticated is not None:
        return flask.redirect(flask.url_for("wallet.dashboard"))
    else:
        return flask.redirect(flask.url_for("auth.connection"))
    
@auth.route("/register", methods=["GET", "POST"])
def register():
    form = CreateUserForm()
    if form.validate_on_submit():
        if global_exist(UserInfo.username, form.username.data) == False:
            try:
                db.session.add(UserInfo(form.username.data, generate_password_hash(form.password.data, method='pbkdf2:sha256', salt_length=8)))
                db.session.commit()
                return flask.redirect(flask.url_for("auth.connection"))
            except exc.IntegrityError:
                db.session.rollback()
                return "This user is alive in our database"
        else:
            flask.flash("Invalid input", category = "error")    
    return flask.render_template("register.html", form = form)
    
@auth.route("/connection",methods=["GET", "POST"])
def connection():
    form = UserForm()
    if form.validate_on_submit():
        if global_exist(UserInfo.username, form.username.data) == True:
            user = UserInfo.query.filter_by(username = form.username.data).first()
            if check_password_hash(user.password, form.password.data) == False:
                flask.flash("Account not found", category = "error")
            else:
                rem = form.remember.data
                if rem:
                    login_user(user, remember=True)
                else:
                    login_user(user, remember=False)
                return flask.redirect(flask.url_for("wallet.dashboard"))
        else:
            flask.flash("Account not found", category = "error")
    return flask.render_template("login.html", form = form)
    
@auth.route("/logout")
def logout():
   logout_user()
   return flask.redirect("/connection")

     
@auth.route("/changeprofile", methods=["GET", "POST"])
def changeprofile():
    form = CheckUserForm()
    if form.validate_on_submit():
        if global_exist(UserInfo.username, form.username.data) == True:
            new_data_user = UserInfo.query.filter_by(username = form.username.data).first()
            new_data_user.password = generate_password_hash(form.password.data, method='pbkdf2:sha256', salt_length=8)
            if totp.verify(form.two_factor_auth.data) == True :
                try:
                    db.session.commit()
                except exc.IntegrityError:
                    db.session.rollback()
                return flask.redirect(flask.url_for("auth.connection"))
            else:
                flask.flash("Incorrect submit password", category="error")
        else:
            flask.flash("This account doesn't exict or user invalid input", category="error")
    return flask.render_template("change_info.html", form=form)  

@auth.route("/two_factor", methods=["GET", "POST"])
def two_factor():
    two_factor_form = TwoFactor()
    if two_factor_form.validate_on_submit():
        if global_exist(UserInfo.username, two_factor_form.email_data.data) == True:
            submit_verification()
            return flask.redirect(flask.url_for("auth.changeprofile"))
        else:
            flask.flash("This account doesn't exict", category="error")
    return flask.render_template("two_factor.html", two_factor_form=two_factor_form)
      


@auth.route("/send_message", methods=["GET", "POST"])
def submit_verification():
     msg = Message("Confirm code", sender=DATA1, recipients = [DATA2])
     msg.body = totp.now()
     mail_sender.send(msg)
     return "Message is sending..."

