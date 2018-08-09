from blueprints import event_bp
from flask import current_app,jsonify, g
from flask_restless.helpers import to_dict
from werkzeug.exceptions import BadRequest, Unauthorized


def login_user(table_proxy):
    if 'username' not in g.request_data or 'password' not in g.request_data:
        raise BadRequest('Username or password not specified')
    return table_proxy.pss_users.get_pss_user_for_event(1,username=g.request_data.get('username', None))    
        
    
@event_bp.route('/login_user', methods=["PUT"])
def login_user_route():
    
    return jsonify({'data':login_user(current_app.table_proxy)}) 

