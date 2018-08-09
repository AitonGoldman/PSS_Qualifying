def generate_pss_users_event_roles_mappings_model(db_handle):
    class PssUsersEventRolesMappings(db_handle.Model):
        pss_user_id=db_handle.Column('pss_user_id', db_handle.Integer, db_handle.ForeignKey('pss_users.pss_user_id'),primary_key=True)
        event_role_id=db_handle.Column('event_role_id', db_handle.Integer, db_handle.ForeignKey('event_roles.event_role_id'),primary_key=True)
        event_id=db_handle.Column('event_id', db_handle.Integer, db_handle.ForeignKey('events.event_id'),primary_key=True)
        event_roles = db_handle.relationship('EventRoles',lazy="joined")
        events = db_handle.relationship('Events',lazy="joined")
    return PssUsersEventRolesMappings
