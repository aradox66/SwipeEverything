from flask import render_template

from app.auth.routes import login_required
from app.errors import bp


@bp.errorhandler(500)
@login_required
def internal_error(error):
    return render_template('errors/500.html'), 500
