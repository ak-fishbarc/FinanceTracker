def add_expense(username, db, category, item, price, date):
    expense_db = db.cx['expenses']
    expense = {'category': category, 'item': item, 'price': price, 'date': date}
    return expense_db[username].insert_one(expense)


def delete_expense(username, db, expense_id):
    expense_db = db.cx['expenses']
    return expense_db[username].delete_one({"_id": expense_id})
