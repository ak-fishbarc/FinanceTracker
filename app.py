from flask import Flask, render_template, redirect, url_for
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from forms import LoginForm


app = Flask(__name__)
app.config.from_object(Config)
limiter = Limiter(key_func=get_remote_address, app=app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


@app.route('/')
def home_page():
    return render_template("home_page.html")


@app.route('/login', methods=['POST', 'GET'])
@limiter.limit("5 per minute")
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect(url_for('home_page'))
    return render_template("login.html", form=form)


@app.route('/register', methods=['POST', 'GET'])
def register():
    return "Register"


@app.errorhandler(429)
def rate_limit_handler(e):
    return "Rate limit exceeded!"


if __name__ == "__main__":
    app.run(debug=True)
