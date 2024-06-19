import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bcrypt import bcrypt
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(100), unique = True, nullable = False)
    password = db.Column(db.String(100), nullable = False)
    email = db.Column(db.String(100), unique = True, nullable = False)

    def __repr__(self):
        return f'{self.username}'


class Services(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable = False)
    price = db.Column(db.Integer, nullable = False)
    isActive = db.Column(db.Boolean, default = True)

    def __repr__(self):
        return f'{self.title}'


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username = username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        mail = User.query.filter_by(email = email.data).first()
        if mail:
            raise ValidationError('That username is taken. Please choose a different one.')
        

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


with app.app_context():
    db.create_all()


@app.route('/')
def index():
    items = Services.query.order_by(Services.price).all()
    return render_template('index.html', data=items)


@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/registre', methods = ['GET', "POST"])
def registre_user():
    if request.method == 'POST':
        ...



@app.route('/login', methods = ['GET', "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=True)
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route('/create', methods = ['POST', 'GET'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        price = request.form['price']
        
        item = Services(title=title, price=price )
        try:
            db.session.add(item)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            print(str(e))
            return 'There is an error'

    else:
        return render_template('create.html')
    
@app.route('/buy/<int:id>')
def buy(id):
    return f'Felecitations {id}'

if __name__ == '__main__':
    app.run(debug=True)