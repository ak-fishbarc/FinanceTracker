from flask import Blueprint
from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_user, logout_user
import sqlalchemy
from urllib.parse import urlsplit
import forms


def create_user_sql_interactions_blueprint(app, db, user_model, limiter):

    user_sql_interactions_blueprint = Blueprint('user_sql_interactions', __name__, template_folder='templates')

    @app.route('/login', methods=['POST', 'GET'])
    @limiter.limit("5 per second")
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('home_page'))
        form = forms.LoginForm()
        if form.validate_on_submit():
            user = db.session.scalar(sqlalchemy.select(user_model).where(user_model.username == form.username.data))
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
        form = forms.create_registration_form(db, user_model)
        if form.validate_on_submit():
            user = user_model(username=form.username.data, email=form.email.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('Registration was successful')
            return redirect(url_for('login'))
        return render_template('registration.html', form=form)

    return user_sql_interactions_blueprint
