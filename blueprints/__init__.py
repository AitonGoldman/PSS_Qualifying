from flask import Blueprint

# blueprint for endpoints that require a tournament id
tournament_bp = Blueprint('tournament', __name__)

# blueprint for endpoints that require a event id
event_bp = Blueprint('event', __name__)
