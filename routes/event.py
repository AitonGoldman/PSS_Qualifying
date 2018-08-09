from blueprints import event_bp
from flask import current_app,jsonify
from flask_restless.helpers import to_dict
from werkzeug.exceptions import BadRequest, Unauthorized
from lib.auth import permissions

@event_bp.route('/event', methods=["PUT"])
def edit_event_route():    
    return jsonify({}) 

@event_bp.route('/event', methods=["POST"])
def add_event_route():
    permission = permissions.EventCreatorPermission()        
    if permission.can():                    
        return jsonify({}) 
    else:
        raise Unauthorized('You are not authorized to do this')
    
@event_bp.route('/event', methods=["GET"])
def get_events_route():                    
    current_app.table_proxy.events_proxy.get_events()
    return jsonify({}) 

@event_bp.route('/event/<int:event_id>', methods=["GET"])
def get_event_route(event_id):                    
    return jsonify({}) 


