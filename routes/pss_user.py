from blueprints import event_bp
from flask import current_app,jsonify, g
from flask_restless.helpers import to_dict
from werkzeug.exceptions import BadRequest, Unauthorized, NotFound
from lib.auth import permissions
from proxies import TableProxyError
from flask_login import current_user
from flask_principal import identity_changed, Identity
from constants.serializers import SERIALIZE_FULL_PSS_USER

def update_pss_user(table_proxy,request_data,event_id):
    # TODO : get the existing user, check that the roles for everything BUT the event_id have not changes
    #        and reject if another events info has been changed

    # TODO : get existing user, check that event_creator has not changed, reject if it changed
    # TODO : prevent editing of event_creator
    
    updated_pss_user,updated_pss_user_dict = table_proxy.pss_users.update_pss_user(request_data)
    table_proxy.commit_changes()

    #the de-serializer doesn't fully fill in the pss_user, so we need to get it after updating
    updated_pss_user = table_proxy.pss_users.get_pss_user(pss_user_id=updated_pss_user.pss_user_id,serialized=False)
    return updated_pss_user.to_dict(extend=SERIALIZE_FULL_PSS_USER)
    

#TODO : implement
def update_event_creator():
    pass

def generate_username(pss_user_dict):
    if pss_user_dict.get("first_name",None) and pss_user_dict.get("last_name",None):
        return pss_user_dict.get("first_name")+pss_user_dict.get("last_name")                 
    else:
        return None
    
def create_event_creator(table_proxy,request_data):    
    request_data['username']=generate_username(request_data)
    new_event_creator= table_proxy.pss_users.create_event_creator(request_data,serialized=False)    
    table_proxy.commit_changes()
    return new_event_creator.to_dict(extend=SERIALIZE_FULL_PSS_USER)
    
def create_pss_user(table_proxy,request_data,event_id,role_id):        
    request_data['username']=generate_username(request_data)
    new_pss_user= table_proxy.pss_users.create_pss_user(request_data,event_id=event_id,role_id=role_id,serialized=False)
    table_proxy.commit_changes()
    return new_pss_user.to_dict(extend=SERIALIZE_FULL_PSS_USER)

@event_bp.route('/event_creator', methods=["POST"])
def create_event_creator_route():                    
    # TODO : need to prevent spamming of this endpoint with itsdangerous safegaurds            
    dict_to_return = create_event_creator(current_app.table_proxy,g.request_data)
    return jsonify({'data':dict_to_return})

#TODO : make role_id part of post?  that would require refactoring incoming request data to be nested (i.e. request['data']['pss_data'])
@event_bp.route('/event/<int:event_id>/pss_user/role/<int:role_id>', methods=["POST"])
def create_pss_user_route(event_id,role_id):                    
    event_edit_permission = permissions.EventEditPermission(event_id)
    if not event_edit_permission.can():
        raise Unauthorized('You are not authorized to add users to this event')             
    dict_to_return = create_pss_user(current_app.table_proxy,g.request_data,event_id,role_id)
    return jsonify({'data':dict_to_return})

@event_bp.route('/event/<int:event_id>/pss_user', methods=["PUT"])
def update_pss_user_route(event_id):                    
    event_edit_permission = permissions.EventEditPermission(event_id)
    if not event_edit_permission.can():
        raise Unauthorized('You are not authorized to add users to this event')    
    dict_to_return = update_pss_user(current_app.table_proxy,g.request_data,event_id)
    return jsonify({'data':dict_to_return})
