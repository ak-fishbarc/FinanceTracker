from flask import Blueprint
from flask import render_template, redirect, url_for
from flask_login import current_user, login_required
import nosql_functions as nf
import forms
import bson


def create_user_nosql_interactions_blueprint(app, db2):
    user_nosql_interactions = Blueprint('user_nosql_interactions', __name__, template_folder='templates')

    @app.route('/post_expense', methods=['POST', 'GET'])
    @login_required
    def post_expense():
        form = forms.ExpenseForm()
        if form.validate_on_submit():
            nf.add_expense(current_user.username, db2, form.category.data, form.item.data,
                           form.price.data, form.expense_date.data)
            return redirect(url_for('get_expense'))
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
        nf.delete_expense(current_user.username, db2, expense_id)
        return redirect(url_for('get_expense'))

    return user_nosql_interactions
