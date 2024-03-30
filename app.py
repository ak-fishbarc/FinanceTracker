from flask import Flask, render_template
from config import Config
from flask_sqlalchemy import SQLAlchemy
from forms import LoginForm

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy()


@app.route('/')
def home_page():
    return render_template("home_page.html")


@app.route('/login', methods=['POST', 'GET'])
def login():
    return render_template("login.html", form=LoginForm())


@app.route('/register', methods=['POST', 'GET'])
def register():
    return "Register"


if __name__ == "__main__":
    app.run(debug=True)
