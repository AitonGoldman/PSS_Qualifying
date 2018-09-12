from blueprints import event_bp
from flask import current_app,jsonify, g, request
from werkzeug.exceptions import BadRequest, Unauthorized
from flask_login import login_user as flask_login_user,logout_user as flask_logout_user, current_user
from flask_principal import identity_changed, Identity

#TODO : need to move passwords for non event creators to usereventmapping object
def login_user(app, request_data):
    if 'username' not in request_data or 'password' not in request_data:
        raise BadRequest('Username or password not specified')    
    username = request_data.get('username', None)
    password = request_data.get('password', None)
    pss_user,pss_user_dict = app.table_proxy.pss_users.get_pss_user(username=username)
    if not pss_user or not pss_user.verify_password(password):
        raise Unauthorized('Bad password')
    flask_logout_user()
    if flask_login_user(pss_user) is False:
        raise Unauthorized('User is not active')
    identity_changed.send(app._get_current_object(), identity=Identity(pss_user.pss_user_id))
    return pss_user_dict

@event_bp.route('/login_user', methods=["PUT"])
def login_user_route():    
    return jsonify({'data':login_user(current_app,g.request_data)})
