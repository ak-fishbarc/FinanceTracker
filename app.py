from flask import Flask, render_template, redirect, url_for, flash
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from config import Config
import sqlalchemy
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, current_user, login_user, logout_user
from forms import LoginForm
import models

app = Flask(__name__)
app.config.from_object(Config)
limiter = Limiter(key_func=get_remote_address, app=app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)


@app.route('/')
def home_page():
    return render_template("home_page.html")


@app.route('/login', methods=['POST', 'GET'])
@limiter.limit("5 per second")
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home_page'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(sqlalchemy.select(models.User).where(models.User.username == form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user)
        return redirect(url_for('home_page'))
    return render_template("login.html", form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home_page'))


@app.route('/register', methods=['POST', 'GET'])
def register():
    return "Register"


@app.errorhandler(429)
def rate_limit_handler(e):
    return "Rate limit exceeded!"


@login_manager.user_loader
def load_user(user):
    return db.session.get(models.User, int(user))


if __name__ == "__main__":
    app.run(debug=True)



