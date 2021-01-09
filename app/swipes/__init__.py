from flask import Blueprint

bp = Blueprint('swipes', __name__)

from app.swipes import routes
