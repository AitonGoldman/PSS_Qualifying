from blueprints import event_bp
from flask import current_app,jsonify, g
from flask_restless.helpers import to_dict
from werkzeug.exceptions import BadRequest, Unauthorized, NotFound
from lib.auth import permissions

def create_event(table_proxy,event_dict):
    if table_proxy.events_proxy.get_event(serialized=False,event_name=event_dict.get('event_name',None)):
        raise BadRequest('Event by that name already exists')
    event = current_app.table_proxy.events_proxy.create_event(event_dict, serialized=False)
    if event is None:
        raise NotFound("Could not create event with configuration options submitted")
    table_proxy.commit_changes()
    return event.to_dict()

@event_bp.route('/event', methods=["POST"])
def create_event_route():                    
    event_create_permission = permissions.EventCreatorPermission()
    if not event_create_permission.can():                
        raise Unauthorized('You are not authorized to create an event')
    dict_to_return = create_event(current_app.table_proxy,g.request_data)
    return jsonify({'data':dict_to_return})

@event_bp.route('/event_template', methods=["GET"])
def get_event_template_route():
    dict_to_return = current_app.table_proxy.events_proxy.get_event_template()
    return jsonify({'data':dict_to_return})

@event_bp.route('/event/<int:event_id>', methods=["GET"])
def get_event_route(event_id):                    
    event, dict_to_return = current_app.table_proxy.events_proxy.get_event(event_id=event_id)
    if event is None:
        raise NotFound("Invalid event id")
    return jsonify({'data':dict_to_return}) 


