from blueprints import event_bp
from flask import current_app,jsonify
from flask_restless.helpers import to_dict
from werkzeug.exceptions import BadRequest, Unauthorized, NotFound

def get_event(table_proxy,event_id):
  event, dict_to_return = table_proxy.events_proxy.get_event(event_id=event_id)
  if event is None:
    raise NotFound("Invalid event id")
  return dict_to_return

@event_bp.route('/event/<int:event_id>', methods=["GET"])
def get_event_route(event_id):                    
  dict_to_return = get_event(current_app.table_proxy, event_id) 
  return jsonify({'data':dict_to_return}) 
