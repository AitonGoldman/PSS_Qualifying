from blueprints import event_bp
from flask import current_app,jsonify
from flask_restless.helpers import to_dict


@event_bp.route('/event_settings', methods=["POST"])
def add_event_settings_route():
    new_event_setting_one = current_app.table_proxy.event_settings.add_event_setting("test_event_1",commit=True)    
    new_event_setting_two = current_app.table_proxy.event_settings.add_event_setting("test_event_2",commit=True)    
    new_event_setting_three = current_app.table_proxy.event_settings.add_event_setting("test_event_3",commit=True)    
    return jsonify({}) 

@event_bp.route('/event', methods=["POST"])
def add_event_route():
    new_event = current_app.table_proxy.events.add_event("test_event_1")
    event_settings = current_app.table_proxy.event_settings.get_event_settings()    
    new_setting_association = current_app.table_proxy.event_settings_association(extra_data="poop")
    new_setting_association.event_setting=event_settings[0]
    new_event.event_settings_values.append(new_setting_association)        
    current_app.table_proxy.commit_changes()
    return jsonify({}) 

@event_bp.route('/event', methods=["GET"])
def get_event_route():                    
    events = current_app.table_proxy.events.get_events()    
    current_app.table_proxy.events.get_event_setting(events[0],'test_event_1').extra_data    
    current_app.table_proxy.events.get_event_setting(events[0],'test_event_1').extra_data
    events = current_app.table_proxy.events.get_events()    
    return jsonify({'event':''}) 


