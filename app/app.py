from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy  import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_login import (LoginManager, UserMixin, login_user, login_required,
    logout_user, current_user)
from werkzeug.security import generate_password_hash, check_password_hash
from classes import LoginForm, PredictForm, RegisterForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    response = None
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('model'))
        response = 'Invalid username or password'
    return render_template('login.html', form=form, response=response)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    response = None
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data,
            method='sha256')
        new_user = User(username=form.username.data, email=form.email.data,
            password=hashed_password)
        if User.query.filter_by(username=new_user.username).first():
            response = 'Please enter a unique username.'
        elif User.query.filter_by(email=new_user.email).first():
            response = 'Please enter a unique email address.'
        else:
            db.session.add(new_user)
            db.session.commit()
            response = 'New user has been created!'
    return render_template('signup.html', form=form, response=response)

@app.route('/model', methods=['GET', 'POST'])
@login_required
def model():
    response = None
    form = PredictForm()
    if form.validate_on_submit():
        return redirect(url_for('outcome'))
    return render_template('model.html', form=form, name=current_user.username)

@app.route('/outcome')
@login_required
def outcome():
    return render_template('outcome.html', name=current_user.username)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
