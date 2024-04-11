from flask import Flask, render_template
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_pymongo import PyMongo
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from models import create_user_model
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
user_model = create_user_model(db)

app.register_blueprint(create_errors_blueprint(app, db))
app.register_blueprint(create_user_sql_interactions_blueprint(app, db, user_model, limiter))
app.register_blueprint(create_user_nosql_interactions_blueprint(app, db2))


@app.before_request
def init_db():
    with app.app_context():
        db.create_all()
        db.session.commit()


@app.route('/')
@app.route('/home_page')
def home_page():
    return render_template("home_page.html")


@login_manager.user_loader
def load_user(user):
    return db.session.get(user_model, int(user))


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")



