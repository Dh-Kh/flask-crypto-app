from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, IntegerField, FloatField
from wtforms.widgets import PasswordInput
from wtforms.validators import DataRequired, Email, EqualTo, Length
class UserForm(FlaskForm):
    username = StringField("username", [DataRequired(), Email()])
    password = StringField(validators=[DataRequired(), Length(min=8, max=64)], widget=PasswordInput())
    remember = BooleanField("remember me")
    submit = SubmitField("submit")
    
class CreateUserForm(FlaskForm):
    username = StringField("username", [DataRequired(), Email()])
    password = StringField(validators=[DataRequired(), Length(min=8, max=64)], widget=PasswordInput())
    confirm_password = StringField(validators=[DataRequired(message="*Required"), EqualTo('password')], widget=PasswordInput())
    submit = SubmitField("submit")

class CheckUserForm(FlaskForm):
    username = StringField("username", [DataRequired(), Email()])
    password = StringField(validators=[DataRequired(), Length(min=8, max=64)], widget=PasswordInput())
    two_factor_auth = StringField("two_factor_auth", validators=[DataRequired()])
    submit = SubmitField("submit")

class WalletValidator(FlaskForm):
    data = StringField("data", [DataRequired(), Length(min=6, max=64)])
    submit = SubmitField("submit")

class WalletTransactions(FlaskForm):
    key_data = StringField("key_data", validators=[DataRequired(), Length(min=8, max=64)])
    commit_id = IntegerField("commit_id", validators=[DataRequired()])
    receiver = StringField("receiver", validators=[DataRequired()])
    sum_data = FloatField("sum_data", validators=[DataRequired()])
    submit = SubmitField("submit")
    
class InputTransaction(FlaskForm):
    key_data = StringField("key_data", validators=[DataRequired(), Length(min=8, max=64)])
    sum_data = FloatField("sum_data", validators=[DataRequired()])
    submit = SubmitField("submit")
    
class TwoFactor(FlaskForm):
    email_data = StringField("username", [DataRequired(), Email()])
    submit = SubmitField("submit")

class TronMoney(FlaskForm):
    tron_wallet_form = StringField("tron_wallet_form", validators=[DataRequired()])
    amount = FloatField("amount", validators=[DataRequired()])
    submit = SubmitField("submit")    

class CashForm(FlaskForm):
    key_data = StringField("key_data", validators=[DataRequired(), Length(min=8, max=64)])
    commit_id = IntegerField("commit_id", validators=[DataRequired()])
    two_factor_auth = StringField("two_factor_auth", validators=[DataRequired()])
    sum_data = FloatField("sum_data", validators=[DataRequired()])
    card_number = IntegerField("card_number", validators=[DataRequired()])
    submit = SubmitField("submit")