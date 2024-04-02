from flask import Flask, render_template, redirect, url_for, flash, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from config import Config
import sqlalchemy
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, current_user, login_user, logout_user
from urllib.parse import urlsplit
import models
import forms

app = Flask(__name__)
app.config.from_object(Config)
limiter = Limiter(key_func=get_remote_address, app=app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


@app.route('/')
@app.route('/home_page')
def home_page():
    return render_template("home_page.html")


@app.route('/login', methods=['POST', 'GET'])
@limiter.limit("5 per second")
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home_page'))
    form = forms.LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(sqlalchemy.select(models.User).where(models.User.username == form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('home_page')
        return redirect(next_page)
    return render_template("login.html", form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home_page'))


@app.route('/register', methods=['POST', 'GET'])
def registration():
    if current_user.is_authenticated:
        return redirect(url_for('home_page'))
    form = forms.RegistrationForm()
    if form.validate_on_submit():
        user = models.User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration was successful')
        return redirect(url_for('login'))
    return render_template('registration.html', form=form)


@app.errorhandler(429)
def rate_limit_handler(error):
    return render_template('429.html'), 429


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    with app.app_context():
        db.session.rollback()
        return render_template('500.html'), 500


@login_manager.user_loader
def load_user(user):
    return db.session.get(models.User, int(user))


if __name__ == "__main__":
    app.run(debug=True)



