from flask import Blueprint, render_template


def create_errors_blueprint(app, db):
    errors = Blueprint('errors', __name__, template_folder='templates')

    @app.errorhandler(429)
    def rate_limit_handler(error):
        return render_template('429.html'), 429

    @app.errorhandler(404)
    def not_found(error):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('500.html'), 500

    return errors
