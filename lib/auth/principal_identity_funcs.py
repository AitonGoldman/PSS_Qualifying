from flask_principal import identity_loaded
from flask_login import current_user
from lib.auth import needs,roles_constants

def generate_pss_user_loader(app):
    @app.login_manager.user_loader
    def load_user(userid):
        return app.table_proxy.pss_users.get_pss_user(pss_user_id=int(userid),serialized=False)
    return load_user

def generate_pss_user_identity_loaded(app):
    @identity_loaded.connect_via(app)
    def on_identity_loaded(sender, identity):
        """Set up the Flask-Principal stuff for this user"""
        if current_user.is_anonymous():            
            return
        if current_user.event_creator:
            identity.provides.add(needs.EventCreatorRoleNeed())
            
            for event in app.table_proxy.events_proxy.get_events_created_by_user(current_user.pss_user_id,serialized=False):
                identity.provides.add(needs.EventEditNeed(event.event_id))

    return on_identity_loaded
