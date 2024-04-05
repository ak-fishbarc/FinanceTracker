from flask import Flask, render_template, redirect, url_for, flash, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from config import Config
import sqlalchemy
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from urllib.parse import urlsplit
from flask_pymongo import PyMongo
import models
import forms
import bson
from errors import errors_blueprint

app = Flask(__name__)
app.config.from_object(Config)
limiter = Limiter(key_func=get_remote_address, app=app)
db = SQLAlchemy(app)
db2 = PyMongo(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

app.register_blueprint(errors_blueprint(app, db))

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


@app.route('/post_expense', methods=['POST', 'GET'])
@login_required
def post_expense():
    form = forms.ExpenseForm()
    if form.validate_on_submit():
        models.add_expense(current_user.username, form.category.data, form.item.data,
                           form.price.data, form.expense_date.data)
        return redirect(url_for('post_expense'))
    return render_template('post_expense.html', form=form)


@app.route('/get_expense')
@login_required
def get_expense():
    expense_db = db2.cx['expenses']
    data = expense_db[current_user.username].find()
    return render_template('get_expense.html', data=data)


@app.route('/update_expense/<expense_id>', methods=['POST', 'GET'])
@login_required
def update_expense(expense_id):
    expense_db = db2.cx['expenses']
    datum = expense_db[current_user.username].find_one_or_404({"_id": bson.ObjectId(expense_id)})
    form = forms.ExpenseForm()
    if form.validate_on_submit():
        expense_db[current_user.username].update_one({"_id": bson.ObjectId(expense_id)},
                                                     {"$set": {"category": form.category.data, "item": form.item.data,
                                                      "price": form.price.data, "expense_date": form.expense_date.data}})
        return redirect(url_for('get_expense'))
    return render_template('update_expense.html', form=form, datum=datum)


@app.route('/delete_expense/<expense_id>')
@login_required
def delete_expense(expense_id):
    expense_id = bson.ObjectId(expense_id)
    models.delete_expense(current_user.username, expense_id)
    return redirect(url_for('get_expense'))


@login_manager.user_loader
def load_user(user):
    return db.session.get(models.User, int(user))


if __name__ == "__main__":
    app.run(debug=True)



