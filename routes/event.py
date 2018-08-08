from blueprints import event_bp
from flask import current_app,jsonify
from flask_restless.helpers import to_dict

@event_bp.route('/event', methods=["PUT"])
def edit_event_route():    
    return jsonify({}) 

@event_bp.route('/event', methods=["POST"])
def add_event_route():
    return jsonify({}) 

@event_bp.route('/event', methods=["GET"])
def get_events_route():                    
    return jsonify({}) 

@event_bp.route('/event/<int:event_id>', methods=["GET"])
def get_events_route(event_id):                    
    return jsonify({}) 


