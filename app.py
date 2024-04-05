from flask import Flask, render_template
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_pymongo import PyMongo
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import models
from errors import create_errors_blueprint
from user_sql_interactions import create_user_sql_interactions_blueprint
from user_nosql_interactions import create_user_nosql_interactions_blueprint

app = Flask(__name__)
app.config.from_object(Config)
limiter = Limiter(key_func=get_remote_address, app=app)
db = SQLAlchemy(app)
db2 = PyMongo(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

app.register_blueprint(create_errors_blueprint(app, db))
app.register_blueprint(create_user_sql_interactions_blueprint(app, db, limiter))
app.register_blueprint(create_user_nosql_interactions_blueprint(app, db2))


@app.route('/')
@app.route('/home_page')
def home_page():
    return render_template("home_page.html")


@login_manager.user_loader
def load_user(user):
    return db.session.get(models.User, int(user))


if __name__ == "__main__":
    app.run(debug=True)



