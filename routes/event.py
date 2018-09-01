from blueprints import event_bp
from flask import current_app,jsonify, g
from flask_restless.helpers import to_dict
from werkzeug.exceptions import BadRequest, Unauthorized, NotFound
from lib.auth import permissions
from proxies import TableProxyError
from flask_login import current_user
from flask_principal import identity_changed, Identity

def update_event(table_proxy,event_dict):
    event_id = event_dict.get("event_id")
    if table_proxy.events_proxy.get_event(serialized=False,event_id=event_id) is None:
        raise BadRequest('Event does not exist')
    updated_event, updated_event_dict = table_proxy.events_proxy.update_event(event_dict)
    table_proxy.commit_changes()
    return updated_event_dict

def create_event(table_proxy,event_dict,pss_user_id):
    if table_proxy.events_proxy.get_event(serialized=False,event_name=event_dict.get('event_name',None)):
        raise BadRequest('Event by that name already exists')
    try:
        event = table_proxy.events_proxy.create_event(event_dict, pss_user_id, serialized=False)
    except TableProxyError as e:        
        raise BadRequest("Failed to create event - experienced the following error : "+str(e))        
    table_proxy.commit_changes()    
    return event.to_dict()

@event_bp.route('/event', methods=["POST"])
def create_event_route():                    
    event_create_permission = permissions.EventCreatorPermission()
    if not event_create_permission.can():                
        raise Unauthorized('You are not authorized to create an event')    
    dict_to_return = create_event(current_app.table_proxy,g.request_data,current_user.pss_user_id)

    return jsonify({'data':dict_to_return})

@event_bp.route('/event', methods=["PUT"])
def update_event_route():                
    event_id = g.request_data.get('event_id',None)    
    event_edit_permission = permissions.EventEditPermission(event_id)
    if not event_edit_permission.can():
        raise Unauthorized('You are not authorized to edit this event')
    dict_to_return = update_event(current_app.table_proxy,g.request_data)
    return jsonify({'data':dict_to_return}) 

def get_event_template(table_proxy):
    return table_proxy.events_proxy.get_event_template()

@event_bp.route('/event_template', methods=["GET"])
def get_event_template_route():    
    return jsonify({'data':get_event_template(current_app.table_proxy)})

def get_event(table_proxy,event_id):
    event, dict_to_return = table_proxy.events_proxy.get_event(event_id=event_id)
    if event is None:
        raise NotFound("Invalid event id")
    return dict_to_return

@event_bp.route('/event/<int:event_id>', methods=["GET"])
def get_event_route(event_id):                    
    dict_to_return = get_event(current_app.table_proxy,event_id)
    return jsonify({'data':dict_to_return}) 


