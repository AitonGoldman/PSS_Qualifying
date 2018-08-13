from blueprints import event_bp
from flask import current_app,jsonify
from flask_restless.helpers import to_dict
from werkzeug.exceptions import BadRequest, Unauthorized, NotFound

@event_bp.route('/event/<int:event_id>', methods=["GET"])
def get_event_route(event_id):                    
    event, dict_to_return = current_app.table_proxy.events_proxy.get_event(event_id=event_id)
    if event is None:
        raise NotFound("Invalid event id")
    return jsonify({'data':dict_to_return}) 


