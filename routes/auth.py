from blueprints import event_bp
from flask import current_app,jsonify, g, request
from flask_restless.helpers import to_dict
from werkzeug.exceptions import BadRequest, Unauthorized
from flask_login import login_user as flask_login_user,logout_user as flask_logout_user, current_user
from flask_principal import identity_changed, Identity

def login_user(table_proxy):
    if 'username' not in g.request_data or 'password' not in g.request_data:
        raise BadRequest('Username or password not specified')    
    username = g.request_data.get('username', None)
    password = g.request_data.get('password', None)
    pss_user,pss_user_dict = table_proxy.pss_users.get_pss_user(username=username)
    if not pss_user or not pss_user.verify_password(password):
        raise Unauthorized('Bad password')
    flask_logout_user()
    if flask_login_user(pss_user) is False:
        raise Unauthorized('User is not active')
    identity_changed.send(current_app._get_current_object(), identity=Identity(pss_user.pss_user_id))
    return pss_user_dict

@event_bp.route('/login_user', methods=["PUT"])
def login_user_route():    
    return jsonify({'data':login_user(current_app.table_proxy)})
