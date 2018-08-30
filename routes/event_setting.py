from blueprints import event_bp
from flask import current_app,jsonify, g
from werkzeug.exceptions import BadRequest, Unauthorized, NotFound
from lib.auth import permissions
from proxies import TableProxyError

def create_event_setting(table_proxy,event_setting_dict):
    if table_proxy.event_settings_proxy.get_event_setting(serialized=False,event_setting_name=event_setting_dict.get('event_setting_name',None)):
        raise BadRequest('Event setting by that name already exists')
    try:
        event_setting = table_proxy.event_settings_proxy.create_event_setting(event_setting_dict['event_setting_name'], serialized=False)
    except TableProxyError as e:
        #TODO : need a problem error handler here
        raise BadRequest(e)
    #TODO : will event_setting ever be none?
    if event_setting is None:
        raise NotFound("Could not create event setting with configuration options submitted")
    table_proxy.commit_changes()
    return event_setting.to_dict()

@event_bp.route('/event_setting', methods=["POST"])
def create_event_setting_route():                    
    #TODO : remove this
    dict_to_return = create_event_setting(current_app.table_proxy,g.request_data)    
    return jsonify({'data':dict_to_return})
    
@event_bp.route('/event_setting', methods=["GET"])
def get_event_setting_route():                    
    event, dict_to_return = current_app.table_proxy.events_proxy.get_event(event_id=event_id)
    if event is None:
        raise NotFound("Invalid event id")
    return jsonify({'data':dict_to_return}) 


